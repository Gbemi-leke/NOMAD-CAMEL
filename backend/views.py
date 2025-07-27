from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.timezone import now
from django.conf import settings
from backend.forms import *
from backend.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from frontend.models import *
from django.forms import modelformset_factory
from django.contrib.auth.models import User
from django.db.models import Count
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth import update_session_auth_hash




def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get("email-username")  # email or username input
        password = request.POST.get("password")
        remember_me = request.POST.get("remember-me")

   
        user = None
        try:
            user_obj = User.objects.get(email=identifier)
            username = user_obj.username
            user = authenticate(request, username=username, password=password)
        except User.DoesNotExist:
           
            user = authenticate(request, username=identifier, password=password)

        if user is not None:
            login(request, user)
            
            # If remember_me is not checked, session expires on browser close
            if not remember_me:
                request.session.set_expiry(0)  # expires on browser close
            else:
                request.session.set_expiry(None)  # default session expiry
            
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('backend:dashboard') 
        else:
            messages.error(request, "Invalid email/username or password.")

    return render(request, "backend/login.html")



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()

            # Handle Profile data if you have extra fields
            profile = Profile.objects.get(user=user)
            profile.phone = form.cleaned_data.get('phone')
            profile.gender = form.cleaned_data.get('gender')
            profile.profile_photo = form.cleaned_data.get('profile_photo')
            profile.address = form.cleaned_data.get('address')
            profile.save()

            # Build email content
            subject = "Welcome to NOMAD-CAMEL 🐪⚡"
            from_email = settings.EMAIL_HOST_USER
            to_email = user.email
            text_content = f"Hi {user.username}, welcome to NOMAD-CAMEL."
            html_content = render_to_string("backend/welcome.html", {
                "user": user,
                "year": now().year
            })

            # Send email
            email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            email.attach_alternative(html_content, "text/html")
            email.send()

            messages.success(request, "Account created successfully! A welcome email has been sent.")
            return redirect('backend:login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'backend/register.html', {'form': form})

@login_required(login_url='/backend/login/')
def logout_view(request):
    logout(request)
    return redirect('index')

@login_required(login_url='/backend/login/')
def dashboard(request):
    
    total_users = User.objects.count()
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()

    # New users per week for last 6 weeks
    today = now().date()
    weeks = []
    users_per_week = []
    for i in range(5, -1, -1):  
        start_week = today - timedelta(days=today.weekday()) - timedelta(weeks=i)
        end_week = start_week + timedelta(days=6)
        count = User.objects.filter(date_joined__date__gte=start_week, date_joined__date__lte=end_week).count()
        weeks.append(start_week.strftime('%b %d'))
        users_per_week.append(count)


    products = Product.objects.all()
    product_names = [p.name for p in products]
    product_quantities = [p.quantity for p in products]

    context = {
        'total_users': total_users,
        'total_products': total_products,
        'active_products': active_products,
        'weeks': weeks,
        'users_per_week': users_per_week,
        'product_names': product_names,
        'product_quantities': product_quantities,
        # 'recent_orders': recent_orders,  # 
    }
    return render(request, 'backend/index.html', context)

@login_required(login_url='/backend/login/')
def add_product(request):
    product = None
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        image_form = ProductImageForm(request.POST, request.FILES)
        size_form = ProductSizeForm(request.POST)

        if product_form.is_valid() and image_form.is_valid() and size_form.is_valid():
            product = product_form.save()

            size = size_form.save(commit=False)
            size.product = product
            size.save()

            images = request.FILES.getlist('images')
            for img in images:
                ProductImage.objects.create(product=product, image=img)

            # ✅ Show success message and keep form in edit mode
            messages.success(request, 'Product added successfully! You can now continue editing it.')

            # Re-initialize forms with the saved product for editing
            product_form = ProductForm(instance=product)
            size_form = ProductSizeForm(instance=size)
            image_form = ProductImageForm()
            
            product_images = ProductImage.objects.filter(product=product)

            context = {
                'product_form': product_form,
                'image_form': image_form,
                'size_form': size_form,
                'context_action': 'Update Product',  
                'product': product,
                'product_images': product_images,
      
            }
            return render(request, 'backend/add-products.html', context)

    else:
        product_form = ProductForm()
        image_form = ProductImageForm()
        size_form = ProductSizeForm()
        
        product_images = ProductImage.objects.filter(product=product)

    context = {
        'product_form': product_form,
        'image_form': image_form,
        'size_form': size_form,
        'context_action': 'Add Product',
       
    }
    return render(request, 'backend/add-products.html', context)

@login_required(login_url='/backend/login/')
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    try:
        size = ProductSize.objects.get(product=product)
    except ProductSize.DoesNotExist:
        size = None

    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        size_form = ProductSizeForm(request.POST, instance=size)
        image_form = ProductImageForm(request.POST, request.FILES)  # for adding new images

        if product_form.is_valid() and size_form.is_valid() and image_form.is_valid():
            product = product_form.save()

            size = size_form.save(commit=False)
            size.product = product
            size.save()

            # Add new images if uploaded
            images = request.FILES.getlist('images')
            for img in images:
                ProductImage.objects.create(product=product, image=img)
            messages.success(request, 'Product editted successfully!')
            return redirect('backend:product-list')

    else:
        product_form = ProductForm(instance=product)
        size_form = ProductSizeForm(instance=size)
        image_form = ProductImageForm()

    context = {
        'product_form': product_form,
        'size_form': size_form,
        'image_form': image_form,
        'product': product,
    }
    return render(request, 'backend/edit-products.html', context)

@login_required(login_url='/backend/login/')
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect('backend:product-list')

@login_required(login_url='/backend/login/')
def product_list(request):
    products = Product.objects.all()
    return render(request, 'backend/view-product-list.html', {'products': products})

@login_required(login_url='/backend/login/')
def user_list(request):
    users = User.objects.all().order_by('username')
    return render(request, 'backend/view-user.html', {'users': users})

@login_required(login_url='/backend/login/')
def add_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'User added successfully.')
            return redirect('backend:user_list')
    else:
        form = RegisterForm()
    return render(request, 'backend/add-user.html', {'form': form})

@login_required(login_url='/backend/login/')
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=user, user_id=user.pk)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('backend:user-list')
    else:
        form = EditUserForm(instance=user, user_id=user.pk)

    return render(request, 'backend/edit-user.html', {'form': form, 'user': user})


@login_required(login_url='/backend/login/')
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('backend:user_list')
    
@login_required(login_url='/backend/login/')
def view_orders(request):
    return render(request, 'backend/view-orders.html')

@login_required(login_url='/backend/login/')
def account(request):
    return render(request, 'backend/account-details.html')

@login_required(login_url='/backend/login/')
def edit_account(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = EditAccount(request.POST, request.FILES, instance=user, user_id=user.pk)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            form = EditAccount(instance=user, user_id=user.pk)
    else:
        form = EditAccount(instance=user, user_id=user.pk)
    return render(request, 'backend/edit-account-details.html', {'form': form, 'user': user})

@login_required(login_url='/backend/login/')
def delete_account(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Account deleted successfully.')
        return redirect('index')

@login_required(login_url='/backend/login/')
def change_password(request):
    if request.method == 'POST':
        change_password = PasswordChangeForm(data=request.POST,
        user=request.user)
        if change_password.is_valid():
            change_password.save()
            update_session_auth_hash(request, change_password.user)
            messages.success(request, 'Password changed successfully.')
    else:
        change_password = PasswordChangeForm(user=request.user)
    return render(request, 'backend/change-password.html', {'pass_key':change_password})
