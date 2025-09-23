from django.contrib.auth import views as auth_views
from django.urls import path
# from django.conf.urls import url 
from backend import views

app_name = 'backend'

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('register', views.register, name='register'),
    path('logout_view-page/', views.logout_view, name='logout_view'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('products/', views.product_list, name='product-list'),
    path('products/add/', views.add_product, name='add-product'),
    path('delete_products/', views.del_products, name='del_products'),
    path('view_products_details/<int:view_id>', views.view_products_details, name='view_products_details'),
    path('products/edit/<int:pk>/', views.edit_product, name='edit-product'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete-product'),
    path('users/', views.user_list, name='user-list'),
    path('users/add/', views.add_user, name='add-user'),
    path('users/edit/<int:pk>/', views.edit_user, name='edit-user'),
    path('users/delete/<int:pk>/', views.delete_user, name='delete-user'),
    path('view-orders', views.view_orders, name='view_orders'),
    path('account', views.account, name='account'),
    path('edit-account/<int:pk>/', views.edit_account, name='edit_account'),
    path('delete-account', views.delete_account, name='delete_account'),
    path('account-change-password', views.change_password, name='change_password'),
    path('account/delete/', views.delete_account, name='delete-account'),
    path('my-wishlist', views.wishlist_view, name='wish'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_cart, name='remove_from_cart'),
    path("checkout/", views.checkout, name="checkout"),
    path("checkout/process/", views.process_checkout, name="process_checkout"),
#     path('product-image/<int:pk>/delete/', views.delete_product_image, name='delete_product_image'),


    # Password reset
    path('password_reset/', views.password_reset_request, name='password_reset_request'),


]