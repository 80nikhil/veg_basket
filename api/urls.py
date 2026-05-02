from django.urls import path
from .views import *

urlpatterns = [
    path('user/register/', RegisterView.as_view(), name='user-register'),
    path('user/login/', LoginView.as_view(), name='user-login'),
    path('user/referral-info/<int:user_id>/', ReferralInfoView.as_view(), name='user-referral-info'),
    path('user/referral-history/<int:user_id>/', ReferralHistoryView.as_view(), name='user-referral-history'),
    path('user/societies/', SocietyListView.as_view(), name='get-all-societies'),
    path('product/categories/', CategoryListView.as_view(), name='get-categories'),
    path('product/products/', ProductListView2.as_view(), name='get-products'),
    path('product/products/category/<int:category_id>/', ProductByCategoryView2.as_view(), name='get-products-by-category'),
    path('product/flash-sales/', FlashSaleListView2.as_view(), name='get-flash-sales'),
    path('product/favorites/<int:favorite_flag>/', FavoriteProductsView.as_view(), name='get-favorite-products'),
    path('product/products/<int:user_id>/', ProductListView.as_view(), name='get-products'),
    path('product/products/category/<int:category_id>/<int:user_id>/', ProductByCategoryView.as_view(), name='get-products-by-category'),
    path('product/flash-sales/<int:user_id>/', FlashSaleListView.as_view(), name='get-flash-sales'),
    path('order/place-order/', PlaceOrderView.as_view(),name='place-order/'),
    path('order/user-orders/', UserOrdersView.as_view(),name='user-orders/'),
    path('order/order-items/', OrderItemsView.as_view(),name='order-items/'),

#------NEW API V2-----------------
    path('cities_list/',CitiesView.as_view(),name="cities_list"),
    path('wallet_history/',WalletHistoryView.as_view(),name='wallet_history'),
    path('get_address/<str:user_id>/',AddressView.as_view(),name='get_address'),
    path('update_address/',AddressView.as_view(),name='update_address'),
    path('get_profile/<str:user_id>/',ProfileView.as_view(),name='get_profile'),
    path('update_profile/',ProfileView.as_view(),name='update_profile'),
    path('update_order_payment_status/',UpdateOrderPaymentStatusView.as_view(),name='update_order_payment_status'),
    path('update_wallet/',UpdateWalletView.as_view(),name='update_wallet'),
    path('get_slots/',GetSlotsView.as_view(),name='get_slots'),
    path('create_order/',CreateOrderView.as_view(),name='create_order'),
    path('get_banners/',GetBanners.as_view(),name='get_banners'),
    path('cancel_order/<str:order_id>/',CancelOrderView.as_view(),name='cancel_order'),
    path('get_related_products/<int:product_id>/',GetRelatedProducts.as_view(),name='get_related_products'),
    path('mostly_ordered_products/<str:user_id>/',MostlyOrderedProductsView.as_view(),name='mostly_ordered_products'),
]
