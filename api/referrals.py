from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from .models import Order, Referral, Settings, User, WalletHistory


DEFAULT_REFERRER_REWARD = Decimal('40.00')
DEFAULT_FRIEND_REWARD = Decimal('30.00')
DEFAULT_MIN_ORDER = Decimal('199.00')
DEFAULT_INVITE_BASE = "https://vegbasket.app/invite/"


def get_decimal_setting(key, default):
    try:
        return Settings.objects.get(key=key).value
    except Settings.DoesNotExist:
        Settings.objects.create(key=key, value=default)
        return default


def get_referral_settings():
    return {
        'min_order': get_decimal_setting('referral_min_order', DEFAULT_MIN_ORDER),
        'referrer_reward': get_decimal_setting('referral_referrer_reward', DEFAULT_REFERRER_REWARD),
        'friend_reward': get_decimal_setting('referral_friend_reward', DEFAULT_FRIEND_REWARD),
    }


def build_referral_invite_link(code):
    return f"{DEFAULT_INVITE_BASE}{code}"


def build_referral_share_message(user):
    invite_link = build_referral_invite_link(user.referal_code)
    settings = get_referral_settings()
    return (
        "VegBasket Fresh Fruits & Vegetables\n\n"
        f"Use my invite link and get Rs. {settings['friend_reward']} cashback on your first order.\n"
        "Fresh fruits & vegetables delivered at your home.\n\n"
        f"Download VegBasket App now:\n{invite_link}\n\n"
        f"Cashback on first order of Rs. {settings['min_order']} or more."
    )


def create_referral_for_user(user, referrer):
    if not referrer or referrer.id == user.id:
        return None

    user.referred_by = referrer
    user.save(update_fields=['referred_by'])
    referral, _ = Referral.objects.get_or_create(
        referred_user=user,
        defaults={'referrer': referrer}
    )
    return referral


@transaction.atomic
def process_referral_for_delivered_order(order):
    referral = getattr(order.user, 'referral_record', None)
    if not referral or referral.status != 'pending':
        return referral

    earlier_delivered_exists = Order.objects.filter(
        user=order.user,
        order_status='delivered',
        created_at__lt=order.created_at
    ).exists()
    if earlier_delivered_exists:
        referral.status = 'invalid'
        referral.save(update_fields=['status'])
        return referral

    settings = get_referral_settings()
    referral.order = order
    referral.order_value = order.total_amount
    referral.reward_referrer = settings['referrer_reward']
    referral.reward_friend = settings['friend_reward']

    if order.total_amount < settings['min_order']:
        referral.status = 'invalid'
        referral.save(update_fields=['order', 'order_value', 'reward_referrer', 'reward_friend', 'status'])
        return referral

    referral.status = 'credited'
    referral.credited_at = timezone.now()
    referral.save(
        update_fields=[
            'order',
            'order_value',
            'reward_referrer',
            'reward_friend',
            'status',
            'credited_at',
        ]
    )

    referral.referrer.wallet_amount += settings['referrer_reward']
    referral.referrer.save(update_fields=['wallet_amount'])
    order.user.wallet_amount += settings['friend_reward']
    order.user.save(update_fields=['wallet_amount'])

    WalletHistory.objects.create(
        user=referral.referrer,
        amount=settings['referrer_reward'],
        payment_type='credit',
        performed_by=None,
    )
    WalletHistory.objects.create(
        user=order.user,
        amount=settings['friend_reward'],
        payment_type='credit',
        performed_by=None,
    )
    return referral
