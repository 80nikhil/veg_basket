from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

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
        return f"{self.name} - ${self.quantity} {self.unit.name}"

class FlashSale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='flash_sales')
    product_flash_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_in_stock = models.BooleanField(default=True)

    def __str__(self):
        return f"Flash Sale: {self.product.name} - ${self.product_flash_price}"
