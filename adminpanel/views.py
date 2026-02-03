from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from api.models import *
from django.views import View
from django.views.generic import ListView
from django.contrib import messages

class TermsAndPolicyViewset(View):
    get_template = 'terms_and_conditions.html'

    def get(self, request):
        return render(request, self.get_template)
    
class SupportViewset(View):
    get_template = 'support.html'

    def get(self, request):
        return render(request, self.get_template)
    
class HomepageViewset(View):
    get_template = 'website/home_page.html'  

    def get(self, request):
        return render(request, self.get_template)
    
class LoginViewset(View):
    get_template = 'website/login.html'  

    def get(self, request):
        return render(request, self.get_template)

class RegisterViewset(View):
    get_template = 'website/register.html'  

    def get(self, request):
        return render(request, self.get_template)  

class LogoutViewset(View):

    def get(self, request):
        return redirect('/login')

class AdminDashboard(View):
    get_template = 'adminpanel/dashboard.html'

    def get(self, request):
        return render(request, self.get_template)

# ================= CATEGORY =================

class CategoryListView(ListView):
    model = Category
    template_name = 'adminpanel/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(is_deleted=False)


class CategoryCreateView(View):
    def post(self, request):
        Category.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            image=request.FILES.get('image')
        )
        messages.success(request, "Category added successfully ✅")
        return redirect('category_list')


class CategoryUpdateView(View):
    def post(self, request, pk):
        cat = get_object_or_404(Category, pk=pk)

        cat.name = request.POST.get('name')
        cat.description = request.POST.get('description')

        if request.FILES.get('image'):
            cat.image = request.FILES.get('image')

        cat.save()
        messages.success(request, "Category updated ✏️")
        return redirect('category_list')


class CategoryDeleteView(View):
    def post(self, request, pk):
        cat = get_object_or_404(Category, pk=pk)
        cat.is_deleted = True
        cat.save()
        messages.success(request, "Category deleted 🗑️")
        return redirect('category_list')


# ================= PRODUCT =================

class ProductListView(View):
    model = Product
    template_name = 'adminpanel/product_list.html'
    context_object_name = 'products'

    def get(self,request, **kwargs):
        context = {}
        context['categories'] = Category.objects.filter(is_deleted=False)
        context['units'] = Unit.objects.all()
        return render(request,self.template_name,context)


class ProductCreateView(View):
    def post(self, request):
        Product.objects.create(
            category_id=request.POST.get('category'),
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            image=request.FILES.get('image'),
            price=request.POST.get('price'),
            quantity=request.POST.get('quantity'),
            unit_id=request.POST.get('unit')
        )
        messages.success(request, "Product added successfully 🛒")
        return redirect('product_list')


class ProductUpdateView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        product.category_id = request.POST.get('category')
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity')
        product.unit_id = request.POST.get('unit')

        if request.FILES.get('image'):
            product.image = request.FILES.get('image')

        product.save()
        messages.success(request, "Product updated ✏️")
        return redirect('product_list')


class ProductDeleteView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_deleted = True
        product.save()
        messages.success(request, "Product deleted 🗑️")
        return redirect('product_list')
