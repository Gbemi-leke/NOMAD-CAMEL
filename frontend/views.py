from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from frontend.models import *

# Create your views here.

def index(request):
    products = Product.objects.all()
    return render(request, 'frontend/index.html', {'pro': products})

def about(request):
    return render(request, 'frontend/about.html')

def product(request):
    products = Product.objects.all()
    return render(request, 'frontend/product.html', {'pro': products})

def contact(request):
    return render(request, 'frontend/contact.html')

def cart(request):
    return render(request, 'frontend/shoping-cart.html')