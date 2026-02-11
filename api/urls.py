from django.urls import path
from .views import *

urlpatterns = [
    path('user/register/', RegisterView.as_view(), name='user-register'),
    path('user/login/', LoginView.as_view(), name='user-login'),
    path('user/societies/', SocietyListView.as_view(), name='get-all-societies'),
    path('product/categories/', CategoryListView.as_view(), name='get-categories'),
    path('product/products/', ProductListView.as_view(), name='get-products'),
    path('product/products/category/<int:category_id>/', ProductByCategoryView.as_view(), name='get-products-by-category'),
    path('product/flash-sales/', FlashSaleListView.as_view(), name='get-flash-sales'),
    path('order/place-order/', PlaceOrderView.as_view(),name='place-order/'),
    path('order/user-orders/', UserOrdersView.as_view(),name='user-orders/'),
    path('order/order-items/', OrderItemsView.as_view(),name='order-items/'),

#------NEW API V2-----------------
    path('cities_list',CitiesView.as_view(),name="cities_list"),
    path('wallet_history',WalletHistoryView.as_view(),name='wallet_history')
]
