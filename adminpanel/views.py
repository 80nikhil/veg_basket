from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from api.models import *
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect
from api.models import WalletHistory

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
        try:
            User.objects.get(id=request.session.get('user_id'))
            return render(request, self.get_template)
        except:
            return redirect('/login/')

class LoginViewset(View):
    template_name = 'website/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email_id=email,password=password)
            request.session['user_id'] = user_obj.id
            request.session['username'] = user_obj.username
            request.session['role'] = user_obj.role
            if user_obj.role == 'admin':
               return redirect('dashboard')
            else:
                return redirect('/')
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return render(request, self.template_name)

class RegisterViewset(View):
    get_template = 'website/register.html'

    def get(self, request):
        return render(request, self.get_template)
    
    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return render(request, self.get_template)

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, self.get_template)

        user_obj = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            role='customer'
        )
        request.session['user_id'] = user_obj.id
        request.session['username'] = user_obj.username
        request.session['role'] = user_obj.role
        messages.success(request, "Admin registered successfully")

        return redirect('dashboard')

class LogoutViewset(View):
    def get(self, request):
        request.session.flush()
        return redirect('/login')

class AdminDashboard(View):
    get_template = 'adminpanel/dashboard.html'

    def get(self, request):
        try:
            User.objects.get(id=request.session.get('user_id'))
            return render(request, self.get_template)
        except:
            return redirect('/login/')

# ================= CATEGORY =================

class CategoryListView(ListView):
    model = Category
    template_name = 'adminpanel/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        try:
            User.objects.get(id=self.request.session.get('user_id'))
            return Category.objects.filter(is_deleted=False)
        except: 
            return redirect('/login/')
        


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
        try:
            User.objects.get(id=request.session.get('user_id')) 
            context = {}
            context['categories'] = Category.objects.filter(is_deleted=False)
            context['units'] = Unit.objects.all()
            return render(request,self.template_name,context)
        except:
            return redirect('/login/')


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
    

#================= Society =========================#

class SocietyListView(ListView):
    model = Society
    template_name = 'adminpanel/society_list.html'
    context_object_name = 'societies'

    def get_queryset(self):
        try:
            User.objects.get(id=self.request.session.get('user_id'))
            return Society.objects.all()
        except: 
            return redirect('/login/')
        
class SocietyCreateView(View):
    def post(self, request):
        Society.objects.create(
            name=request.POST.get('name'),
        )
        messages.success(request, "Society added successfully ✅")
        return redirect('society_list')

class SocietyUpdateView(View):
    def post(self, request, pk):
        society = get_object_or_404(Society, pk=pk)

        society.name = request.POST.get('name')
        society.save()
        messages.success(request, "Society updated ✏️")
        return redirect('society_list')
    
class SocietyDeleteView(View):
    def post(self, request, pk):
        society = get_object_or_404(Society, pk=pk)
        society.delete()
        messages.success(request, "Society deleted 🗑️")
        return redirect('society_list')
    
    
#================= Unit =========================#

class UnitListView(ListView):
    model = Unit
    template_name = 'adminpanel/unit_list.html'
    context_object_name = 'units'

    def get_queryset(self):
        try:
            User.objects.get(id=self.request.session.get('user_id'))
            return Unit.objects.all()
        except: 
            return redirect('/login/')
        
class UnitCreateView(View):
    def post(self, request):
        Unit.objects.create(
            name=request.POST.get('name'),
        )
        messages.success(request, "Unit added successfully ✅")
        return redirect('unit_list')    
    
class UnitUpdateView(View):
    def post(self, request, pk):
        unit = get_object_or_404(Unit, pk=pk)

        unit.name = request.POST.get('name')
        unit.save()
        messages.success(request, "Unit updated ✏️")
        return redirect('unit_list')

class UnitDeleteView(View):
    def post(self, request, pk):
        unit = get_object_or_404(Unit, pk=pk)
        unit.delete()
        messages.success(request, "Unit deleted 🗑️")
        return redirect('unit_list')

#================= Flash Sale =========================#

class FlashSaleListView(ListView):
    model = FlashSale
    template_name = 'adminpanel/flash_sale_list.html'
    context_object_name = 'flash_sales'

    def get_queryset(self):
        try:
            User.objects.get(id=self.request.session.get('user_id'))
            return FlashSale.objects.all()
        except: 
            return redirect('/login/')

class FlashSaleCreateView(View):
    def post(self, request):
        FlashSale.objects.create(
            product_id=request.POST.get('product'),
            product_flash_price=request.POST.get('product_flash_price'),
            is_in_stock=request.POST.get('is_in_stock') == 'on'
        )
        messages.success(request, "Flash Sale added successfully ✅")
        return redirect('flash_sale_list')

class FlashSaleUpdateView(View):
    def post(self, request, pk):
        flash_sale = get_object_or_404(FlashSale, pk=pk)

        flash_sale.product_id = request.POST.get('product')
        flash_sale.product_flash_price = request.POST.get('product_flash_price')
        flash_sale.is_in_stock = request.POST.get('is_in_stock') == 'on'
        flash_sale.save()
        messages.success(request, "Flash Sale updated ✏️")
        return redirect('flash_sale_list')

class FlashSaleDeleteView(View):
    def post(self, request, pk):
        flash_sale = get_object_or_404(FlashSale, pk=pk)
        flash_sale.delete()
        messages.success(request, "Flash Sale deleted 🗑️")
        return redirect('flash_sale_list')
    

#================= Order =========================#
class OrderListView(ListView):
    model = Order
    template_name = 'adminpanel/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        try:
            User.objects.get(id=self.request.session.get('user_id'))
            return Order.objects.all()
        except: 
            return redirect('/login/')

class OrderUpdateView(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)

        order.order_status = request.POST.get('order_status')
        order.save()
        messages.success(request, "Order status updated ✏️")
        return redirect('order_list')

#================= User =========================#

class UserListView(ListView):
    model = User
    template_name = 'adminpanel/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        try:
            User.objects.get(id=self.request.session.get('user_id'))
            return User.objects.all()
        except: 
            return redirect('/login/')


class WalletUpdateView(View):
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        amount = Decimal(request.POST.get('amount'))
        payment_type = request.POST.get('payment_type')

        if payment_type == 'credit':
            user.wallet_amount += amount

        elif payment_type == 'debit':
            if user.wallet_amount < amount:
                messages.error(request, "Insufficient wallet balance ❌")
                return redirect('user_list')
            user.wallet_amount -= amount

        user.save()

        WalletHistory.objects.create(
            user=user,
            amount=amount,
            payment_type=payment_type
        )

        messages.success(request, "Wallet updated successfully ✅")
        return redirect('user_list')
    
class WalletHistoryListView(ListView):
    model = WalletHistory
    template_name = 'adminpanel/wallet_history.html'
    context_object_name = 'histories'
    ordering = ['-created_at']

    def get_queryset(self):
        try:
            User.objects.get(id=self.request.session.get('user_id'))
            return WalletHistory.objects.select_related('user', 'performed_by')
        except:
            return redirect('/login/')

