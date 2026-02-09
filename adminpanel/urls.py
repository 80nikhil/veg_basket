from django.urls import path
from . views import *

urlpatterns = [

    path('',HomepageViewset.as_view(),name='homepage'),
    path('terms-and-policy/', TermsAndPolicyViewset.as_view(), name='terms-and-policy'),
    path('support/', SupportViewset.as_view(), name='support'),
    path('register/', RegisterViewset.as_view(), name='register'),
    path('login/', LoginViewset.as_view(), name='login'),
    path('logout/', LogoutViewset.as_view(), name='logout'),
    path('dashboard/', AdminDashboard.as_view(), name='dashboard'),

    # CATEGORY
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),

    # PRODUCT
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),

    # Society
    path('societies/', SocietyListView.as_view(), name='society_list'),
    path('society/create/', SocietyCreateView.as_view(), name='society_create'),  
    path('society/update/<int:pk>/', SocietyUpdateView.as_view(), name='society_update'),
    path('society/delete/<int:pk>/', SocietyDeleteView.as_view(), name='society_delete'),

    #Unit
    path('units/', UnitListView.as_view(), name='unit_list'),
    path('unit/create/', UnitCreateView.as_view(), name='unit_create'),
    path('unit/update/<int:pk>/', UnitUpdateView.as_view(), name='unit_update'),
    path('unit/delete/<int:pk>/', UnitDeleteView.as_view(), name='unit_delete'),

    # Flash Sale
    path('flash-sales/', FlashSaleListView.as_view(), name='flash_sale_list'),
    path('flash-sale/create/', FlashSaleCreateView.as_view(), name='flash_sale_create'),
    path('flash-sale/update/<int:pk>/', FlashSaleUpdateView.as_view(),
            name='flash_sale_update'),
    path('flash-sale/delete/<int:pk>/', FlashSaleDeleteView.as_view(),
            name='flash_sale_delete'),
    
    # Order
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('order/update/<int:pk>/', OrderUpdateView.as_view(), name='order_update'),
    
    #User
    path('users/', UserListView.as_view(), name='user_list'),

    path('wallet/update/<int:user_id>/', WalletUpdateView.as_view(), name='wallet_update'),
    path('wallet/history/', WalletHistoryListView.as_view(), name='wallet_history'),

]