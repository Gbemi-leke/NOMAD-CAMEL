from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

# Create your views here.

def index(request):
    return render(request, 'frontend/index.html')

def about(request):
    return render(request, 'frontend/about.html')

def product(request):
    return render(request, 'frontend/product.html')

def contact(request):
    return render(request, 'frontend/contact.html')