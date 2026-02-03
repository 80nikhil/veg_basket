from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import User, Society
from django.views.decorators.http import require_GET
import json

@require_GET
def get_all_societies(request):
    societies = Society.objects.all().values('id', 'name', 'created_at')
    return JsonResponse({'societies': list(societies)})


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({'error': 'Invalid or missing JSON data.'}, status=400)
        username = data.get('username')
        contact_no = data.get('contact_no')

        if not username or not contact_no:
            return JsonResponse({'error': 'Name and mobile number are required.'}, status=400)

        if User.objects.filter(contact_no=contact_no).exists():
            return JsonResponse({'error': 'Mobile number already registered.'}, status=400)

        user = User.objects.create(username=username, contact_no=contact_no)
        return JsonResponse({'message': 'Registration successful.', 'user_id': user.id,'username':user.username,'contact_no':user.contact_no,'email_id':user.email_id,'referal_code':user.referal_code,'wallet_amount':user.wallet_amount})

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({'error': 'Invalid or missing JSON data.'}, status=400)
        contact_no = data.get('contact_no')

        if not contact_no:
            return JsonResponse({'error': 'Mobile number is required.'}, status=400)

        try:
            user = User.objects.get(contact_no=contact_no)
            return JsonResponse({'message': 'Login successful.', 'user_id': user.id,'username':user.username,'contact_no':user.contact_no,'email_id':user.email_id,'referal_code':user.referal_code,'wallet_amount':user.wallet_amount})
        except User.DoesNotExist:
            return JsonResponse({'error': 'Mobile number not registered. Please register first.'}, status=404)
