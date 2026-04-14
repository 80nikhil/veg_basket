from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from api.models import *
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect
from .utils.firebase import send_firebase_notification
from django.utils.dateparse import parse_date

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
    template_name = 'adminpanel/product_list.html'
    def get(self, request, **kwargs):
        try:
            User.objects.get(id=request.session.get('user_id'))
            context = {}
            context['products'] = Product.objects.filter()
            context['categories'] = Category.objects.filter()
            context['units'] = Unit.objects.all().order_by('-id')
            context['cities'] = City.objects.all().order_by('-id')
            return render(request, self.template_name, context)
        except:
            return redirect('/login/')


class ProductCreateView(View):
    def post(self, request):
        product = Product.objects.create(
            category_id=request.POST.get('category'),
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            image=request.FILES.get('image'),
            price=request.POST.get('price'),
            quantity=request.POST.get('quantity'),
            unit_id=request.POST.get('unit'),
            is_in_stock=True if request.POST.get('is_in_stock') else False
        )
        city_ids = request.POST.getlist('cities')
        product.cities.set(city_ids)
        messages.success(request, "Product added successfully 🛒")
        return redirect('product_list')




class ProductUpdateView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk, is_deleted=False)
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity')
        product.category_id = request.POST.get('category')
        product.unit_id = request.POST.get('unit')
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
        product.is_in_stock = True if request.POST.get('is_in_stock') else False
        product.save()
        city_ids = request.POST.getlist('cities')
        product.cities.set(city_ids)
        messages.success(request, "Product updated successfully ✏️")
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
            return Unit.objects.all().order_by('-id')
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

    def get(self,request):
        try:
            User.objects.get(id=self.request.session.get('user_id'))
            flash_sales = FlashSale.objects.all().order_by('-id')
            products = Product.objects.all().order_by('-id')
            context = {"flash_sales":flash_sales,"products":products}
            return render(request,self.template_name,context)
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

    def get(self, request):
        try:
            User.objects.get(id=self.request.session.get('user_id'))
            orders = Order.objects.all().order_by('-id')[:20]
            delivery_boys = User.objects.filter(role='delivery')
            context = {"orders": orders,"delivery_boys": delivery_boys}
            return render(request, self.template_name, context)
        except:
            return redirect('/login/')

class OrderUpdateView(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order_status = request.POST.get('order_status')
        assigned_to_id = request.POST.get('assigned_to')

        if order_status:
            order.order_status = order_status
        if assigned_to_id:
            order.assigned_to_id = assigned_to_id
        else:
            admin_user = User.objects.filter(role='admin').first()
            order.assigned_to = admin_user
        order.save()

        messages.success(request, "Order updated successfully ✏️")
        return redirect('order_list')

#================= User =========================#

class UserListView(ListView):
    model = User
    template_name = 'adminpanel/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        try:
            User.objects.get(id=self.request.session.get('user_id'))
            return User.objects.all().order_by('-id')
        except: 
            return redirect('/login/')

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

#================= City =========================#
class CityListView(ListView):
    model = City
    template_name = 'adminpanel/city_list.html'
    context_object_name = 'cities'

    def get_queryset(self):
        try:
            User.objects.get(id=self.request.session.get('user_id'))
            return City.objects.all().order_by('-id')
        except: 
            return redirect('/login/')

class CityCreateView(View):
    def post(self, request):
        City.objects.create(
            name=request.POST.get('name'),
            pin_code=request.POST.get('pin_code'),
        )
        messages.success(request, "City added successfully ✅")
        return redirect('city_list')
    
class CityUpdateView(View):
    def post(self, request, pk):
        city = get_object_or_404(City, pk=pk)

        city.name = request.POST.get('name')
        city.pin_code = request.POST.get('pin_code')
        city.save()

        messages.success(request, "City updated ✏️")
        return redirect('city_list')
    
class CityDeleteView(View):
    def post(self, request, pk):
        city = get_object_or_404(City, pk=pk)
        city.delete()
        messages.success(request, "City deleted 🗑️")
        return redirect('city_list')

class SupportView(View):
    template_name = 'support.html'

    def get(self, request):
        try:
            User.objects.get(id=request.session.get('user_id'))
            return render(request, self.template_name)
        except:
            return redirect('/login/')    


class BannerListView(View):
    template_name = "adminpanel/banner_list.html"

    def get(self, request):
        try:
            User.objects.get(id=request.session.get('user_id'))
            banners = Aids_banner.objects.all().order_by('-id')
            return render(request, self.template_name, {"banners": banners})
        except:
            return redirect('/login/')


class BannerCreateView(View):

    def post(self, request):
        try:
            User.objects.get(id=request.session.get('user_id'))
            image = request.FILES.get("image")

            if image:
                Aids_banner.objects.create(image=image)
                messages.success(request, "Banner added successfully")

            return redirect("banner_list")  
        except:
            return redirect('/login/')

class BannerDeleteView(View):

    def post(self, request, pk):
        banner = Aids_banner.objects.get(id=pk)
        banner.delete()

        messages.success(request, "Banner deleted successfully")
        return redirect("banner_list")                  
    

class SendFirebaseNotificationView(View):
    template_name = "adminpanel/send_firebase.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        title = request.POST.get("title")
        body = request.POST.get("body")
        if not title or not body:
            messages.warning(request, "Title and Body are required!")
            return redirect("send_firebase")

        # Get all tokens
        tokens = list(User.objects.values_list("fcm_token", flat=True))

        # If no tokens, send default notification to everyone (or just skip)
        if not tokens:
            # Optionally, define default tokens if you store them somewhere
            messages.warning(request, "No user device tokens found. Sending default notification skipped.")
            return redirect("send_firebase")

        # Send notification
        result = send_firebase_notification(tokens, title, body)

        messages.success(
            request,
            f"Notification sent! Success: {result['success']}, Fail: {result['failure']}"
        )
        return redirect("send_firebase")    
    

class WalletUpdateView(View):
    def post(self, request, user_id):
        amount = Decimal(request.POST.get("amount", 0))
        txn_type = request.POST.get("payment_type")
        user = User.objects.get(id=user_id)

        if txn_type == "credit":
            user.wallet_amount += amount
        elif txn_type == "debit":
            user.wallet_amount -= amount
        user.save()
        WalletHistory.objects.create(
            user=user,
            amount=amount,
            payment_type=txn_type
        )

        return JsonResponse({"success": True, "user_id": user.id, "new_amount": user.wallet_amount})

class WalletUpdateAllView(View):
    def post(self, request):
        amount = float(request.POST.get("amount", 0))
        txn_type = request.POST.get("payment_type")

        updated_wallets = []
        users = User.objects.all()  # Update all records
        for user in users:
            if txn_type == "credit":
                user.wallet_amount += amount
            else:
                user.wallet_amount -= amount
            user.save()
            WalletHistory.objects.create(
                user=user,
                amount=amount,
                payment_type=txn_type
            )
            updated_wallets.append({"id": user.id, "new_amount": user.wallet_amount})

        return JsonResponse({"success": True, "updated_wallets": updated_wallets})    

class SlotPageView(View):
    def get(self, request):
        date = request.GET.get("date")

        slots = SlotMaster.objects.all()
        eliminated = EliminatedSlot.objects.filter(date=date) if date else []

        min_order = Settings.objects.filter(key="min_order").first()
        min_val = min_order.value if min_order else 0

        return render(request, "adminpanel/slot_management.html", {
            "slots": slots,
            "eliminated_slots": eliminated,
            "selected_date": date,
            "min_order": min_val
        })

class EliminateSlotView(View):
    def post(self, request):
        slot_id = request.POST.get("slot_id")
        date = request.POST.get("date")

        EliminatedSlot.objects.get_or_create(slot_id=slot_id, date=date)

        return redirect(f"/slot-management/?date={date}")

class RestoreSlotView(View):
    def post(self, request):
        obj = EliminatedSlot.objects.get(id=request.POST.get("id"))
        date = obj.date
        obj.delete()
        return redirect(f"/slot-management/?date={date}")
    
class CreateSlotView(View):
    def post(self, request):
        SlotMaster.objects.create(
            name=request.POST.get("name"),
            start_time=request.POST.get("start_time"),
            end_time=request.POST.get("end_time")
        )
        return redirect("/slot-management/")    
    
class UpdateMinOrderView(View):
    def post(self, request):
        val = request.POST.get("min_order")

        try:
            obj = Settings.objects.get(key="min_order")
            obj.value = val
            obj.save()
        except Settings.DoesNotExist:
            obj = Settings.objects.create(key="min_order",value=val)
        return redirect("/slot-management/")                    

