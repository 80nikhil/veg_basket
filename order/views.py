from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
import csv
from django.utils import timezone
from datetime import datetime
from decimal import Decimal
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import UserCart
from user.models import User
from product.models import Product
from .models import Order, OrderProduct
from django.db import transaction
from decimal import Decimal
import uuid
from django.views.decorators.http import require_GET
from django.db.models import Sum

@csrf_exempt
@require_POST
def add_to_cart(request):
	try:
		data = json.loads(request.body)
		user_id = data.get('user_id')
		product_id = data.get('product_id')
		if not user_id or not product_id:
			return JsonResponse({'error': 'user_id and product_id are required.'}, status=400)
		user = User.objects.get(id=user_id)
		product = Product.objects.get(id=product_id)
		UserCart.objects.create(user=user, product=product)
		return JsonResponse({'message': 'Product added to cart successfully.'})
	except User.DoesNotExist:
		return JsonResponse({'error': 'User not found.'}, status=404)
	except Product.DoesNotExist:
		return JsonResponse({'error': 'Product not found.'}, status=404)
	except Exception as e:
		return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_GET
def get_cart_products(request):
	user_id = request.GET.get('user_id')
	if not user_id:
		return JsonResponse({'error': 'user_id is required.'}, status=400)
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
		products = list(product_map.values())
		return JsonResponse({'cart_products': products})
	except User.DoesNotExist:
		return JsonResponse({'error': 'User not found.'}, status=404)
	
# Terms and Conditions view
def terms_and_conditions(request):
	return render(request, 'order/terms_and_conditions.html')

# Support page view
def support(request):
	return render(request, 'order/support.html')


@csrf_exempt
@require_POST
def place_order(request):
	try:
		data = json.loads(request.body)
	except Exception:
		return JsonResponse({'error': 'Invalid JSON.'}, status=400)

	user_id = data.get('user_id')
	society_id = data.get('society_id')
	order_value = data.get('order_value')
	address = data.get('address')
	delivery_date = data.get('delivery_date')
	delivery_slot = data.get('delivery_slot')
	products = data.get('products') or []

	if not user_id or not products or not order_value or not address or not society_id or not delivery_date or not delivery_slot:
		return JsonResponse({'error': 'all details are required.'}, status=400)

	try:
		user = User.objects.get(id=user_id)
	except User.DoesNotExist:
		return JsonResponse({'error': 'User not found.'}, status=404)

	# Start DB transaction
	try:
		with transaction.atomic():
			# create Order
			# generate sequential order_id like #0001 based on last created Order.id
			last_order = Order.objects.order_by('-id').first()
			if last_order:
				next_num = last_order.id + 1
			else:
				next_num = 1
			order_id_str = f"{next_num:04d}"

			# create Order
			order = Order.objects.create(
				order_id=order_id_str,
				user=user,
				society_id=society_id if society_id else None,
				address=address,
				delivery_date=delivery_date,
				delivery_slot=delivery_slot,
				total_amount=order_value,
			)

			created_products = []
			for p in products:
				pid = p.get('product_id')
				qty = int(p.get('quantity', 1))
				if not pid or qty <= 0:
					raise ValueError('Invalid product entry in products list.')
				product = Product.objects.get(id=pid)
				# create OrderProduct
				OrderProduct.objects.create(order=order, product=product, quantity=qty)

				cart_qs = UserCart.objects.filter(user=user, product=product, is_order_checked_out=False)
				to_mark = cart_qs[:qty]
				for ci in to_mark:
					ci.is_order_checked_out = True
					ci.save()

				created_products.append({'product_id': product.id, 'quantity': qty})


			return JsonResponse({
				'message': 'Order placed successfully.',
				'order_id': order.order_id,
				'order_db_id': order.id,
				'total_amount': str(order.total_amount),
				'products': created_products,
			})
	except Product.DoesNotExist:
		return JsonResponse({'error': 'One of the products not found.'}, status=404)
	except ValueError as ve:
		return JsonResponse({'error': str(ve)}, status=400)
	except Exception as e:
		return JsonResponse({'error': str(e)}, status=500)


# API 1: Get all orders for a user
@csrf_exempt
@require_GET
def user_orders(request):
	user_id = request.GET.get('user_id')
	if not user_id:
		return JsonResponse({'error': 'user_id is required.'}, status=400)
	try:
		user = User.objects.get(id=user_id)
		orders = Order.objects.filter(user=user).order_by('-created_at')
		data = [
			{
				'order_id': o.order_id,
				'created_at': o.created_at,
				'total_amount': str(o.total_amount),
				'order_status': o.order_status,
				'society_name': o.society.name if o.society else None,
				'address': o.address,
			}
			for o in orders
		]
		return JsonResponse({'orders': data})
	except User.DoesNotExist:
		return JsonResponse({'error': 'User not found.'}, status=404)


# API 2: Get all items for an order
@csrf_exempt
@require_GET
def order_items(request):
	req_order_id = request.GET.get('order_id')
	order_id = req_order_id
	if not order_id:
		return JsonResponse({'error': 'order_id is required.'}, status=400)
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
		return JsonResponse({'order_id': order.order_id, 'items': data})
	except Order.DoesNotExist:
		return JsonResponse({'error': 'Order not found.'}, status=404)


# Admin dashboard: shows all orders with customer data and items (staff only)
@staff_member_required
def admin_dashboard(request):
	# read filters from query params
	start_date = request.GET.get('start_date')  # expected format YYYY-MM-DD
	end_date = request.GET.get('end_date')
	month = request.GET.get('month')  # YYYY-MM for monthly total
	export = request.GET.get('export')  # if 'csv' then return CSV

	orders_qs = Order.objects.select_related('user', 'society').prefetch_related('order_products__product__unit')

	# apply date range filter (supports single day when only start_date provided)
	if start_date:
		try:
			sd = datetime.strptime(start_date, '%Y-%m-%d')
			orders_qs = orders_qs.filter(created_at__date__gte=sd.date())
		except Exception:
			pass
	if end_date:
		try:
			ed = datetime.strptime(end_date, '%Y-%m-%d')
			orders_qs = orders_qs.filter(created_at__date__lte=ed.date())
		except Exception:
			pass

	# if no range provided but month provided, filter by month
	if not start_date and not end_date and month:
		try:
			m = datetime.strptime(month, '%Y-%m')
			orders_qs = orders_qs.filter(created_at__year=m.year, created_at__month=m.month)
		except Exception:
			pass

	# compute total based on active filters:
	# - if date range provided (start_date and/or end_date) -> sum of orders_qs (already filtered)
	# - elif month provided -> sum of that month
	# - else -> sum of ALL orders (user expects reset/empty filters to show full sale amount)
	total_month = Decimal('0.00')
	try:
		if start_date or end_date:
			agg = orders_qs.aggregate(s=Sum('total_amount'))
			total_val = agg.get('s')
		elif month:
			m = datetime.strptime(month, '%Y-%m')
			month_orders = Order.objects.filter(created_at__year=m.year, created_at__month=m.month)
			agg = month_orders.aggregate(s=Sum('total_amount'))
			total_val = agg.get('s')
		else:
			agg = Order.objects.aggregate(s=Sum('total_amount'))
			total_val = agg.get('s')
		if total_val is not None:
			total_month = Decimal(total_val)
	except Exception:
		total_month = Decimal('0.00')

	# prepare data rows
	rows = []
	for o in orders_qs.order_by('-created_at'):
		items = []
		for op in o.order_products.all():
			prod = op.product
			items.append({
				'product_id': prod.id,
				'name': prod.name,
				'unit': prod.unit.name if prod.unit else None,
				'price': str(prod.price),
				'quantity': op.quantity*op.product.quantity,
			})

		rows.append({
			'order_id': o.order_id,
			'created_at': o.created_at,
			'total_amount': str(o.total_amount),
			'order_status': o.order_status,
			'delivery_date': getattr(o, 'delivery_date', None),
			'delivery_slot': getattr(o, 'delivery_slot', None),
			'address': o.address,
			'user': {
				'id': o.user.id,
				'username': o.user.username,
				'contact_no': getattr(o.user, 'contact_no', None),
				'address': getattr(o.user, 'address', None),
			},
			'society': o.society.name if o.society else None,
			'items': items,
			'items_json': json.dumps(items),
		})

	# CSV export
	if export == 'csv':
		# Create CSV response
		response = HttpResponse(content_type='text/csv')
		filename = 'orders_report.csv'
		response['Content-Disposition'] = f'attachment; filename="{filename}"'
		writer = csv.writer(response)
		# header
		writer.writerow(['Order ID', 'Created At', 'User', 'Contact', 'Society', 'Address', 'Delivery Date', 'Delivery Slot', 'Total Amount', 'Status', 'Items'])
		for r in rows:
			items_str = '; '.join([f"{it['name']} x{it['quantity']}" for it in r['items']])
			writer.writerow([r['order_id'], r['created_at'], r['user']['username'], r['user']['contact_no'], r['society'], r['address'], r['delivery_date'], r['delivery_slot'], r['total_amount'], r['order_status'], items_str])
		return response

	return render(request, 'order/admin_dashboard.html', {
		'orders': rows,
		'total_month': str(total_month),
		'filters': {
			'start_date': start_date or '',
			'end_date': end_date or '',
			'month': month or '',
		}
	})

