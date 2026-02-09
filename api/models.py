from decimal import Decimal
from django.db import models


# ================= Society =================
class Society(models.Model):
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ================= User (ONLY ONE USER MODEL) =================
class User(models.Model):
    username = models.CharField(max_length=100)
    email_id = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    referal_code = models.CharField(max_length=15, null=True, blank=True)

    # ✅ Wallet as Decimal
    wallet_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )

    society = models.ForeignKey(
        Society,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )

    address = models.TextField()
    role = models.CharField(
        max_length=50,
        default='customer',
        choices=[('customer', 'customer'), ('admin', 'admin')]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


# ================= Wallet History =================
class WalletHistory(models.Model):
    PAYMENT_CHOICES = (
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='wallet_histories'
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES)

    performed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='wallet_actions_done'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.payment_type} - {self.amount}"


# ================= Category =================
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# ================= Unit =================
class Unit(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# ================= Product =================
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.quantity} {self.unit.name}"


# ================= Flash Sale =================
class FlashSale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='flash_sales')
    product_flash_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_in_stock = models.BooleanField(default=True)

    def __str__(self):
        return f"Flash Sale: {self.product.name} - {self.product_flash_price}"


# ================= Order =================
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    order_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    society = models.ForeignKey(Society, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    address = models.CharField(max_length=200)
    delivery_date = models.CharField(max_length=50, null=True, blank=True)
    delivery_slot = models.CharField(max_length=100, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"


# ================= Order Product =================
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ordered_products')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

