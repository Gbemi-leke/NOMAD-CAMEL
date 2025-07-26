from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from frontend.models import *
from backend.models import*
from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator


# Create your views here.

def index(request):
    all_products = Product.objects.all()
    hot_products = Product.objects.filter(hot=True)
    daily_deals = Product.objects.filter(daily_deal=True)
    
    return render(request, 'frontend/index.html', {
        'pro': all_products,
        'hot': hot_products,
        'deals': daily_deals,
    })
def about(request):
    return render(request, 'frontend/about.html')

def product(request):
    products = Product.objects.all()
    return render(request, 'frontend/product.html', {'pro': products})

def contact(request):
    return render(request, 'frontend/contact.html')

def cart(request):
    return render(request, 'frontend/shoping-cart.html')





def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        # Already exists, so remove it from the wishlist.
        wishlist.delete()
        status = 'removed'
    else:
        status = 'added'
    return JsonResponse({'status': status})


def load_more_products(request):
    page = int(request.GET.get('page', 1))
    per_page = 6  # or however many you want to load per click

    products = Product.objects.all()
    paginator = Paginator(products, per_page)

    try:
        page_obj = paginator.page(page)
    except:
        return JsonResponse({'products': [], 'has_next': False})

    data = []
    for product in page_obj:
        data.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'image_url': product.image.url if product.image else '',
        })

    return JsonResponse({
        'products': data,
        'has_next': page_obj.has_next()
    })
