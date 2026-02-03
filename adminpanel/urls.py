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
]