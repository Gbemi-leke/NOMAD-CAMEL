from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from frontend.models import *
from backend.models import*
from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    all_products = Product.objects.order_by('-created_at')
    hot_products = Product.objects.filter(hot=True)
    daily_deals = Product.objects.filter(daily_deal=True)
    
    return render(request, 'frontend/index.html', {'pro': all_products,'hot': hot_products,'deals': daily_deals,})
def about(request):
    return render(request, 'frontend/about.html')

def product(request):
    products = Product.objects.order_by('-created_at')
    paginator = Paginator(products, 8) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'frontend/product.html', {'page_obj': page_obj})

def product_details(request, product_id):
    product_detail =Product.objects.get(id=product_id)
    return render(request, 'frontend/product-detail.html', {'det':product_detail})


def contact(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        message = request.POST.get('msg')  # match your form field name

        subject = 'Contact Us - NOMAD CAMEL'
        context = {
            'email': email,
            'message': message,
        }
        html_message = render_to_string('frontend/mail-template.html', context)
        plain_message = strip_tags(html_message)
        from_email = 'NOMAD-CAMEL <nomadcamelngpb@gmail.com>'
        recipient_list = [email]  

        try:
            send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
            messages.success(request, 'Email sent, you will receive a response shortly!')
        except Exception as e:
            messages.error(request, f'Mail not sent. Error: {str(e)}')

    return render(request, 'frontend/contact.html')


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



def search_products(request):
    query = request.GET.get('q', '')
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'frontend/search-results.html', context)
