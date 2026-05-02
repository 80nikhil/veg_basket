from rest_framework import serializers
from .models import *


class SocietySerializer(serializers.ModelSerializer):
    class Meta:
        model = Society
        fields = ['id', 'name', 'created_at']

class RegisterSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    society_name = serializers.CharField(source='society.name', read_only=True)
    referrer_code = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'contact_no', 'email_id', 'referal_code', 'wallet_amount','role','society','city','block_flat','city_name','society_name', 'referrer_code']
        read_only_fields = ['id', 'referal_code', 'wallet_amount','role','city_name','society_name']

    def create(self, validated_data):
        validated_data.pop('referrer_code', None)
        validated_data.setdefault('password', '')
        validated_data.setdefault('email_id', '')
        return User.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    contact_no = serializers.CharField()

class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image', 'created_at']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name')
    unit = serializers.CharField(source='unit.name')
    favorite_type_label = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'image','is_in_stock', 'favorite_type', 'favorite_type_label',
            'category_name', 'price', 'quantity', 'unit', 'created_at'
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_favorite_type_label(self, obj):
        return obj.get_favorite_type_display() if obj.favorite_type is not None else None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['price'] = str(data['price'])  # keep price as string
        return data

class FlashSaleSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = FlashSale
        fields = ['id', 'product_flash_price', 'is_in_stock', 'product']

    def get_product(self, obj):
        prod = obj.product
        request = self.context.get('request')
        return {
            'id': prod.id,
            'name': prod.name,
            'description': prod.description,
            'image': request.build_absolute_uri(prod.image.url) if prod.image else None,
            'category': prod.category.name,
            'regular_price': str(prod.price),
            'price': str(obj.product_flash_price),
            'quantity': prod.quantity,
            'unit': prod.unit.name if prod.unit else None,
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['flash_id'] = data.pop('id')  # rename id → flash_id
        data['product_flash_price'] = str(data['product_flash_price'])
        return data

class AddToCartSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    product_id = serializers.IntegerField()

class AddToCartSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    product_id = serializers.IntegerField()

class OrderProductInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

class PlaceOrderSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    society_id = serializers.IntegerField()
    order_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    address = serializers.CharField()
    delivery_date = serializers.DateField()
    delivery_slot = serializers.CharField()
    products = OrderProductInputSerializer(many=True)

class WalletHistoryInputSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)    

class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = address
        fields = '__all__'        

class WalletHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletHistory
        fields = '__all__'  

class ReferralSerializer(serializers.ModelSerializer):
    referrer_name = serializers.CharField(source='referrer.username', read_only=True)
    referred_name = serializers.CharField(source='referred_user.username', read_only=True)
    referred_contact = serializers.CharField(source='referred_user.contact_no', read_only=True)
    order_id = serializers.CharField(source='order.order_id', read_only=True)

    class Meta:
        model = Referral
        fields = [
            'id',
            'referrer_name',
            'referred_name',
            'referred_contact',
            'order_id',
            'order_value',
            'reward_referrer',
            'reward_friend',
            'status',
            'created_at',
            'credited_at',
        ]

class SlotMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlotMaster
        fields = '__all__'

class SeettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = '__all__'   

class AidsBannerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Aids_banner
        fields = ['id', 'image', 'created_at']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None                           
