from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def register_admin(request):
    return render(request, 'adminpanel/register.html')

def login_admin(request):
    return render(request, 'adminpanel/login.html')

def dashboard(request):
    return render(request, 'adminpanel/dashboard.html')
