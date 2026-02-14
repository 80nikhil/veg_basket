from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from .models import *
from .serializers import *
from datetime import datetime as dt

class SocietyListView(APIView):
    def get(self, request):
        societies = Society.objects.all()
        serializer = SocietySerializer(societies, many=True)
        return Response({'societies': serializer.data})

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not request.data.get('username') or not request.data.get('contact_no'):
            return Response(
                {'error': 'Name and mobile number are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(contact_no=request.data.get('contact_no')).exists():
            return Response(
                {'error': 'Mobile number already registered.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Registration successful.',
                'user_id': user.id,
                'username': user.username,
                'contact_no': user.contact_no,
                'email_id': user.email_id,
                'referal_code': user.referal_code,
                'wallet_amount': user.wallet_amount
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'error': 'Mobile number is required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        contact_no = serializer.validated_data['contact_no']

        try:
            user = User.objects.get(contact_no=contact_no)
            return Response({
                'message': 'Login successful.',
                'user_id': user.id,
                'username': user.username,
                'contact_no': user.contact_no,
                'email_id': user.email_id,
                'referal_code': user.referal_code,
                'wallet_amount': user.wallet_amount
            })
        except User.DoesNotExist:
            return Response(
                {'error': 'Mobile number not registered. Please register first.'},
                status=status.HTTP_404_NOT_FOUND
            )

class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.filter(is_deleted=False)
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response({'categories': serializer.data})

class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.filter(is_deleted=False)
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response({'products': serializer.data})

class ProductByCategoryView(APIView):
    def get(self, request, category_id):
        products = Product.objects.filter(category_id=category_id, is_deleted=False)
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response({'products': serializer.data})
    
class FlashSaleListView(APIView):
    def get(self, request):
        flash_items = FlashSale.objects.filter(is_in_stock=True)
        serializer = FlashSaleSerializer(flash_items, many=True, context={'request': request})
        return Response({'flash_sales': serializer.data})

class AddToCartView(APIView):
    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user_id = serializer.validated_data['user_id']
        product_id = serializer.validated_data['product_id']

        try:
            user = User.objects.get(id=user_id)
            product = Product.objects.get(id=product_id)
            UserCart.objects.create(user=user, product=product)
            return Response({'message': 'Product added to cart successfully.'})
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=404)

class CartProductsView(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required.'}, status=400)

        try:
            user = User.objects.get(id=user_id)
            cart_items = UserCart.objects.filter(user=user, is_order_checked_out=False)

            product_map = {}
            for item in cart_items:
                pid = item.product.id
                if pid not in product_map:
                    product_map[pid] = {
                        'cart_id': item.id,
                        'product_id': pid,
                        'product_name': item.product.name,
                        'product_description': item.product.description,
                        'product_image': request.build_absolute_uri(item.product.image.url) if item.product.image else None,
                        'product_price': item.product.price,
                        'order_qty': 1,
                    }
                else:
                    product_map[pid]['order_qty'] += 1
                    product_map[pid]['product_price'] += item.product.price

            return Response({'cart_products': list(product_map.values())})

        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)

class PlaceOrderView(APIView):
    def post(self, request):
        data = request.data.copy()   # make mutable copy
        parsed = dt.strptime(data['delivery_date'], "%d %b")
        current_year = dt.now().year
        final_date = parsed.replace(year=current_year)
        data['delivery_date'] = final_date.date()   # must call ()
        serializer = PlaceOrderSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        data = serializer.validated_data

        try:
            user = User.objects.get(id=data['user_id'])
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)

        try:
            last_order = Order.objects.order_by('-id').first()
            next_num = last_order.id + 1 if last_order else 1
            order_id_str = f"{next_num:04d}"

            order = Order.objects.create(
                order_id=order_id_str,
                user=user,
                society_id=data['society_id'],
                address=data['address'],
                delivery_date=data['delivery_date'],
                delivery_slot=data['delivery_slot'],
                total_amount=data['order_value'],
            )

            created_products = []

            for p in data['products']:
                product = Product.objects.get(id=p['product_id'])
                OrderProduct.objects.create(order=order, product=product, quantity=p['quantity'])
                created_products.append({'product_id': product.id, 'quantity': p['quantity']})

            return Response({
                'message': 'Order placed successfully.',
                'order_id': order.order_id,
                'order_db_id': order.id,
                'total_amount': str(order.total_amount),
                'products': created_products,
            })
        except Product.DoesNotExist:
            return Response({'error': 'One of the products not found.'}, status=404)

class UserOrdersView(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required.'}, status=400)

        try:
            user = User.objects.get(id=user_id)
            orders = Order.objects.filter(user=user).order_by('-created_at')

            data = [{
                'order_id': o.order_id,
                'created_at': o.created_at,
                'total_amount': str(o.total_amount),
                'order_status': o.order_status,
                'society_name': o.society.name if o.society else None,
                'address': o.address,
            } for o in orders]

            return Response({'orders': data})

        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)

class OrderItemsView(APIView):
    def get(self, request):
        order_id = request.GET.get('order_id')
        if not order_id:
            return Response({'error': 'order_id is required.'}, status=400)
        try:
            order = Order.objects.get(order_id=order_id)
            items = OrderProduct.objects.filter(order=order)
            data = []
            for it in items:
                prod = it.product
                data.append({
                    'product_id': prod.id,
                    'name': prod.name,
                    'product_quantity': prod.quantity,
                    'unit': prod.unit.name if prod.unit else None,
                    'price': str(prod.price),
                    'image': request.build_absolute_uri(prod.image.url) if prod.image else None,
                    'order_quantity': it.quantity,
                })

            return Response({'order_id': order.order_id, 'items': data})

        except Order.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=404)
        
#------NEW API V2-----------------

class CitiesView(APIView):
    def get(self,request):
        cities_list = City.objects.all()
        serializer = CitiesSerializer(cities_list,many=True)
        context = {
            'message':"Cities fetched Succesfully",
            'cities': serializer.data
        }
        return Response(context,status=status.HTTP_200_OK)

class WalletHistoryView(APIView):

    @swagger_auto_schema(request_body=WalletHistoryInputSerializer)
    def post(self,request):
        input_serializer = WalletHistoryInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        user_id = input_serializer.validated_data['user_id']
        user_id = request.data.get('user_id')
        try:
            user_obj = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': "User not exist!"}, status=400)

        history = WalletHistory.objects.filter(user=user_obj).order_by("-id")
        history_data = WalletHistorySerializer(history, many=True).data
        user_data = RegisterSerializer(user_obj).data

        return Response({
            'user': user_data,
            'data': history_data
        })