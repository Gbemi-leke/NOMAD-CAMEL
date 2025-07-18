from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

# Create your views here.

def login(request):
    return render(request, 'backend/login.html')

def register(request):
    return render(request, 'backend/register.html')

def dashboard(request):
    return render(request, 'backend/index.html')
