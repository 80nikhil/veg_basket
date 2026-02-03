from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from products.models import Product
from products.forms import ProductForm
from user.models import User  # Added for dashboard stats
from order.models import Order # Added for dashboard stats

# Helper function to check if the user is staff/admin
def is_admin(user):
    return user.is_authenticated and user.is_staff

# --- PRODUCT MANAGEMENT VIEWS ---

@user_passes_test(is_admin, login_url='/adminpanel/login/') 
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

@user_passes_test(is_admin, login_url='/adminpanel/login/')
def product_upsert(request, pk=None):
    instance = get_object_or_404(Product, pk=pk) if pk else None
    form = ProductForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'products/product_form.html', {'form': form})

@user_passes_test(is_admin, login_url='/adminpanel/login/')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
    return redirect('product_list')

# --- ADMIN AUTH VIEWS ---

def register_admin(request):
    # Logic for registering a new admin user could go here
    return render(request, 'adminpanel/register.html')

def login_admin(request):
    if request.method == 'POST':
        # ... your authentication logic here ...
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.is_staff:
                return redirect('dashboard')  # Send Admins to Dashboard
            else:
                return redirect('product_list') # Send Customers to Shop
    return render(request, 'adminpanel/login.html')

def logout_admin(request):
    auth_logout(request)
    # Redirect to the admin login page after logging out
    return redirect('login_admin') 

# --- DASHBOARD VIEW ---

@user_passes_test(is_admin, login_url='/adminpanel/login/')
def dashboard(request):
    # Gathering real-time data for your dashboard cards
    product_count = Product.objects.count()
    user_count = User.objects.count()
    order_count = Order.objects.count()
    low_stock_count = Product.objects.filter(stock__lt=5).count()
    
    context = {
        'product_count': product_count,
        'user_count': user_count,
        'order_count': order_count,
        'low_stock_count': low_stock_count,
    }
    return render(request, 'adminpanel/dashboard.html', context)