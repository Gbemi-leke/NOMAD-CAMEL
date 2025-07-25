from django.urls import path
# from django.conf.urls import url 
from frontend import views

app_name = 'frontend'

urlpatterns = [
    path('', views.about, name='about'),
    path('product', views.product, name='product'),
    path('contact', views.contact, name='contact'),
    path('cart', views.cart, name='cart'),

]