from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Product
from .forms import ProductForm
from .models import Order, OrderItem

# Helper function to check if the user is staff/admin
def is_admin(user):
    return user.is_authenticated and user.is_staff

# 1. READ (Admin Inventory Table)
@user_passes_test(is_admin, login_url='/adminpanel/login/')
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

# 2. CREATE & UPDATE
@user_passes_test(is_admin, login_url='/adminpanel/login/')
def product_upsert(request, pk=None):
    instance = get_object_or_404(Product, pk=pk) if pk else None
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=instance)
    return render(request, 'products/product_form.html', {'form': form})

# 3. DELETE
@user_passes_test(is_admin, login_url='/adminpanel/login/')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})

# 4. PUBLIC SHOP GALLERY
def shop_gallery(request):
    query = request.GET.get('search')
    if query:
        all_veggies = Product.objects.filter(name__icontains=query)
    else:
        all_veggies = Product.objects.all()

    cart = request.session.get('cart', {})
    total_items = sum(cart.values())

    return render(request, 'products/shop_gallery.html', {
        'items': all_veggies,
        'cart': cart,
        'cart_count': total_items
    })

# 5. CART LOGIC (Add)
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    p_id = str(product_id)
    cart[p_id] = cart.get(p_id, 0) + 1
    request.session['cart'] = cart
    return redirect('shop_gallery')

# 6. CART LOGIC (Remove)
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    p_id = str(product_id)
    if p_id in cart:
        if cart[p_id] > 1:
            cart[p_id] -= 1
        else:
            del cart[p_id]
    request.session['cart'] = cart
    return redirect('shop_gallery')

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    grand_total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total_price = product.price * quantity
        grand_total += total_price
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total_price,
        })

    return render(request, 'products/cart_detail.html', {
        'cart_items': cart_items,
        'grand_total': grand_total,
    })

def place_order(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('shop_gallery')

        # Get customer details from form
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        # Calculate Total
        total = 0
        order_items_to_create = []
        for p_id, qty in cart.items():
            product = get_object_or_404(Product, id=p_id)
            total += product.price * qty
            order_items_to_create.append((product, qty))

        # 1. Save the Order
        new_order = Order.objects.create(
            customer_name=name,
            customer_phone=phone,
            address=address,
            total_amount=total
        )

        # 2. Save Order Items
        for product, qty in order_items_to_create:
            OrderItem.objects.create(
                order=new_order,
                product=product,
                quantity=qty,
                price=product.price
            )

        # 3. Clear the Cart
        request.session['cart'] = {}
        
        return render(request, 'products/order_success.html', {'order': new_order})
    
    return redirect('cart_detail')