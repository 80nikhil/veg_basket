from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('societies/', SocietyListView.as_view(), name='get-all-societies'),
    path('categories/', CategoryListView.as_view(), name='get-categories'),
    path('products/', ProductListView.as_view(), name='get-products'),
    path('products/category/<int:category_id>/', ProductByCategoryView.as_view(), name='get-products-by-category'),
    path('flash-sales/', FlashSaleListView.as_view(), name='get-flash-sales'),
    path('place-order/', PlaceOrderView.as_view(),name='place-order/'),
    path('user-orders/', UserOrdersView.as_view(),name='user-orders/'),
    path('order-items/', OrderItemsView.as_view(),name='order-items/'),
]
