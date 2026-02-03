from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register/', views.register_admin, name='register_admin'),
    path('login/', views.login_admin, name='login_admin'),
    path('logout/', views.logout_admin, name='logout_admin'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Inventory Management
    path('inventory/', views.product_list, name='product_list'),
    path('inventory/add/', views.product_upsert, name='product_add'),  # For adding new
    path('inventory/edit/<int:pk>/', views.product_upsert, name='product_edit'),  # For editing
    path('inventory/delete/<int:pk>/', views.product_delete, name='product_delete'),
]