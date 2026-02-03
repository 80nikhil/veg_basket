from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add/', views.product_upsert, name='product_add'),
    path('edit/<int:pk>/', views.product_upsert, name='product_edit'),
    path('delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('shop/', views.shop_gallery, name='shop_gallery'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('place-order/', views.place_order, name='place_order'),
]