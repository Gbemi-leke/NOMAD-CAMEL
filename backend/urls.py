from django.urls import path
# from django.conf.urls import url 
from backend import views

app_name = 'backend'

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('logout_view-page/', views.logout_view, name='logout_view'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('products/', views.product_list, name='product-list'),
    path('products/add/', views.add_product, name='add-product'),
    path('products/edit/<int:pk>/', views.edit_product, name='edit-product'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete-product'),
    path('users/', views.user_list, name='user-list'),
    path('users/add/', views.add_user, name='add-user'),
    path('users/edit/<int:pk>/', views.edit_user, name='edit-user'),
    path('users/delete/<int:pk>/', views.delete_user, name='delete-user'),
    path('account', views.account, name='account'),
    path('edit-account/<int:pk>/', views.edit_account, name='edit_account'),
    path('account-change-password', views.change_password, name='change_password'),

]