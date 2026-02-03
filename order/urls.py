from django.urls import path
from .views import add_to_cart, get_cart_products, terms_and_conditions, support, place_order, user_orders, order_items, admin_dashboard

urlpatterns = [
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('get-cart-products/', get_cart_products, name='get-cart-products'),
    path('terms-and-conditions/', terms_and_conditions, name='terms-and-conditions'),
    path('support/', support, name='support'),
    path('place-order/', place_order, name='place-order'),
    path('user-orders/', user_orders, name='user-orders'),
    path('order-items/', order_items, name='order-items'),
    path('admin-dashboard/', admin_dashboard, name='admin-dashboard'),
]