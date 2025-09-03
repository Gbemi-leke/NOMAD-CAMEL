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
    path('products/edit/<int:pk>/', views.edit_product, name='edit-product'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete-product'),
    path('users/', views.user_list, name='user-list'),
    path('users/add/', views.add_user, name='add-user'),
    path('users/edit/<int:pk>/', views.edit_user, name='edit-user'),
    path('users/delete/<int:pk>/', views.delete_user, name='delete-user'),
    path('view-orders', views.view_orders, name='view_orders'),
    path('account', views.account, name='account'),
    path('edit-account/<int:pk>/', views.edit_account, name='edit_account'),
    path('delete-account/<int:pk>/', views.delete_account, name='delete_account'),
    path('account-change-password', views.change_password, name='change_password'),
    path('account/delete/', views.delete_account, name='delete-account'),
    path('my-wishlist', views.wishlist_view, name='wish'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_cart, name='remove_from_cart'),
    path("checkout/", views.checkout_view, name="checkout"),

    # Password reset
    path("password-reset/", 
         auth_views.PasswordResetView.as_view(template_name="backend/password-reset.html"),
         name="password_reset"),
    
    path("password-reset/done/", 
         auth_views.PasswordResetDoneView.as_view(template_name="backend/password-reset-done.html"),
         name="password_reset_done"),
    
    path("reset/<uidb64>/<token>/", 
         auth_views.PasswordResetConfirmView.as_view(template_name="backend/password-reset-confirm.html"),
         name="password_reset_confirm"),
    
    path("reset/done/", 
         auth_views.PasswordResetCompleteView.as_view(template_name="backend/password-reset-complete.html"),
         name="password_reset_complete"),


]