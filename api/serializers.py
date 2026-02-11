from rest_framework import serializers
from .models import *


class SocietySerializer(serializers.ModelSerializer):
    class Meta:
        model = Society
        fields = ['id', 'name', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'contact_no', 'email_id', 'referal_code', 'wallet_amount']
        read_only_fields = ['id', 'email_id', 'referal_code', 'wallet_amount']


class LoginSerializer(serializers.Serializer):
    contact_no = serializers.CharField()

class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image', 'created_at']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name')
    unit = serializers.CharField(source='unit.name')

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'image',
            'category_name', 'price', 'quantity', 'unit', 'created_at'
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['price'] = str(data['price'])  # keep price as string
        return data

class FlashSaleSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = FlashSale
        fields = ['id', 'product_flash_price', 'is_in_stock', 'product']

    def get_product(self, obj):
        prod = obj.product
        request = self.context.get('request')
        return {
            'id': prod.id,
            'name': prod.name,
            'description': prod.description,
            'image': request.build_absolute_uri(prod.image.url) if prod.image else None,
            'category': prod.category.name,
            'regular_price': str(prod.price),
            'price': str(obj.product_flash_price),
            'quantity': prod.quantity,
            'unit': prod.unit.name if prod.unit else None,
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['flash_id'] = data.pop('id')  # rename id → flash_id
        data['product_flash_price'] = str(data['product_flash_price'])
        return data

class AddToCartSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    product_id = serializers.IntegerField()

class AddToCartSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    product_id = serializers.IntegerField()

class OrderProductInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

class PlaceOrderSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    society_id = serializers.IntegerField()
    order_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    address = serializers.CharField()
    delivery_date = serializers.DateField()
    delivery_slot = serializers.CharField()
    products = OrderProductInputSerializer(many=True)

class WalletHistoryInputSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)    

class CitiesSerializer(serializers.Serializer):
    class Meta:
        model = City
        fields = '__all__'

class WalletHistorySerializer(serializers.Serializer):
    class Meta:
        model = WalletHistory
        fields = '__all__'        