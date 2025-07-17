from django.urls import path
# from django.conf.urls import url 
from backend import views

app_name = 'backend'

urlpatterns = [
    path('login', views.login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),

]