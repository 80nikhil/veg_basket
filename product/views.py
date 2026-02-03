from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .models import Category, Product
from .models import FlashSale

class CategoryListView(View):
    def get(self, request):
        categories = Category.objects.filter(is_deleted=False)
        data = [
            {
                'id': cat.id,
                'name': cat.name,
                'description': cat.description,
                'image': request.build_absolute_uri(cat.image.url) if cat.image else None,
                'created_at': cat.created_at
            }
            for cat in categories
        ]
        return JsonResponse({'categories': data})

class ProductListView(View):
    def get(self, request):
        products = Product.objects.filter(is_deleted=False)
        data = [
            {
                'id': prod.id,
                'name': prod.name,
                'description': prod.description,
                'image': request.build_absolute_uri(prod.image.url) if prod.image else None,
                'category_name': prod.category.name,
                'price': str(prod.price),
                'quantity': prod.quantity,
                'unit': prod.unit.name,
                'created_at': prod.created_at
            }
            for prod in products
        ]
        return JsonResponse({'products': data})

class ProductByCategoryView(View):
    def get(self, request, category_id):
        products = Product.objects.filter(category_id=category_id, is_deleted=False)
        data = [
            {
                'id': prod.id,
                'name': prod.name,
                'description': prod.description,
                'image': request.build_absolute_uri(prod.image.url) if prod.image else None,
                'category_name': prod.category.name,
                'price': str(prod.price),
                'quantity': prod.quantity,
                'unit': prod.unit.name,
                'created_at': prod.created_at
            }
            for prod in products
        ]
        return JsonResponse({'products': data})


class FlashSaleListView(View):
    def get(self, request):
        flash_items = FlashSale.objects.filter(is_in_stock=True)
        data = []
        for f in flash_items:
            prod = f.product
            data.append({
                'flash_id': f.id,
                'product_flash_price': str(f.product_flash_price),
                'is_in_stock': f.is_in_stock,
                'product': {
                    'id': prod.id,
                    'name': prod.name,
                    'description': prod.description,
                    'image': request.build_absolute_uri(prod.image.url) if prod.image else None,
                    'category': prod.category.name,
                    'regular_price': str(prod.price),
                    'price': str(f.product_flash_price),
                    'quantity': prod.quantity,
                    'unit': prod.unit.name if prod.unit else None,
                }
            })
        return JsonResponse({'flash_sales': data})
