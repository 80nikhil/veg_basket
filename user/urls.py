from django.urls import path
from .views import RegisterView, LoginView, get_all_societies

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('societies/', get_all_societies, name='get-all-societies'),
]