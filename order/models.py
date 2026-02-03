from django.db import models
from user.models import User, Society
from product.models import Product

class UserCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_products')
    is_order_checked_out = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

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

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ordered_products')
    quantity = models.PositiveIntegerField()
    # Adding price field so you know what the price was when they bought it
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"