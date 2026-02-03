from django.urls import path
from .views import CategoryListView, ProductListView, ProductByCategoryView, FlashSaleListView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='get-categories'),
    path('products/', ProductListView.as_view(), name='get-products'),
    path('products/category/<int:category_id>/', ProductByCategoryView.as_view(), name='get-products-by-category'),
    path('flash-sales/', FlashSaleListView.as_view(), name='get-flash-sales'),
]