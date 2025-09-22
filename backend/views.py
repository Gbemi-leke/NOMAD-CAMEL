from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.timezone import now
from django.conf import settings
from backend.forms import *
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from backend.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from frontend.models import *
from django.forms import modelformset_factory
from django.contrib.auth.models import User
from django.db.models import Count
from datetime import timedelta
from django.views.decorators.http import require_POST
from django.contrib.auth import update_session_auth_hash
from decimal import Decimal


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
            return redirect('index') 
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
            return redirect('backend:login_view')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'backend/register.html', {'form': form})

@login_required(login_url='/auth/login/')
def logout_view(request):
    logout(request)
    return redirect('index')

@login_required(login_url='/auth/login/')
def dashboard(request):
    products = Product.objects.all()
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
        'products': products,
        'product_quantities': product_quantities,
        # 'recent_orders': recent_orders,  # 
    }
    return render(request, 'backend/index.html', context)

@login_required(login_url='/auth/login/')
def add_product(request):
    product = None
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        image_form = ProductImageForm(request.POST, request.FILES)
        # size_form = ProductSizeForm(request.POST)

        if product_form.is_valid() and image_form.is_valid():
            product = product_form.save()

            # size = size_form.save(commit=False)
            # size.product = product
            # size.save()

            images = request.FILES.getlist('images')
            for img in images:
                ProductImage.objects.create(product=product, image=img)

            # ✅ Show success message and keep form in edit mode
            messages.success(request, 'Product added successfully! You can now continue editing it.')

            # Re-initialize forms with the saved product for editing
            product_form = ProductForm(instance=product)
            # size_form = ProductSizeForm(instance=size)
            image_form = ProductImageForm()
            
            product_images = ProductImage.objects.filter(product=product)

            context = {
                'product_form': product_form,
                'image_form': image_form,
                # 'size_form': size_form,
                'context_action': 'Update Product',  
                'product': product,
                'product_images': product_images,
      
            }
            return render(request, 'backend/add-products.html', context)

    else:
        product_form = ProductForm()
        image_form = ProductImageForm()
        # size_form = ProductSizeForm()
        
        product_images = ProductImage.objects.filter(product=product)

    context = {
        'product_form': product_form,
        'image_form': image_form,
        # 'size_form': size_form,
        'context_action': 'Add Product',
       
    }
    return render(request, 'backend/add-products.html', context)

@login_required(login_url='/auth/login/')
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    

    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        # size_form = ProductSizeForm(request.POST, instance=size)
        image_form = ProductImageForm(request.POST, request.FILES)  # for adding new images

        if product_form.is_valid() and image_form.is_valid():
            product = product_form.save()

            # size = size_form.save(commit=False)
            # size.product = product
            # size.save()

            # Add new images if uploaded
            images = request.FILES.getlist('images')
            for img in images:
                ProductImage.objects.create(product=product, image=img)
            messages.success(request, 'Product editted successfully!')
            return redirect('backend:product-list')

    else:
        product_form = ProductForm(instance=product)
        # size_form = ProductSizeForm(instance=size)
        image_form = ProductImageForm()

    context = {
        'product_form': product_form,
        # 'size_form': size_form,
        'image_form': image_form,
        'product': product,
    }
    return render(request, 'backend/edit-products.html', context)

@login_required(login_url='/auth/login/')
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect('backend:product_list')

@login_required(login_url='/auth/login/')
def product_list(request):
    products = Product.objects.all()
    return render(request, 'backend/view-product-list.html', {'products': products})

@login_required(login_url='/auth/login/')
def user_list(request):
    users = User.objects.all().order_by('username')
    return render(request, 'backend/view-user.html', {'users': users})

@login_required(login_url='/auth/login/')
def add_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'User added successfully.')
            return redirect('backend:user-list')
    else:
        form = RegisterForm()
    return render(request, 'backend/add-user.html', {'form': form})

@login_required(login_url='/auth/login/')
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


@login_required(login_url='/auth/login/')
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('backend:user-list')
    
@login_required(login_url='/auth/login/')
def view_orders(request):
    return render(request, 'backend/view-orders.html')

@login_required(login_url='/auth/login/')
def account(request):
    return render(request, 'backend/account-details.html')

@login_required(login_url='/auth/login/')
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

@login_required(login_url='/auth/login/')
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"status": "ok", "message": "Account deleted successfully."})
        messages.success(request, 'Account deleted successfully.')
        return redirect('index')

    return JsonResponse({"status": "error", "message": "Invalid request."}, status=400)


@login_required(login_url='/auth/login/')
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


@login_required(login_url='/auth/login/')
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  
        user.delete()    
        return redirect('index')  
    return redirect('backend:account')  

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'backend/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def remove_from_wishlist(request, product_id):
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('backend:wish')


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    cart = request.session.get('cart', {})
    pid = str(product_id)

    if pid in cart:
        cart[pid]['quantity'] += quantity
        cart[pid]['subtotal'] = float(cart[pid]['quantity'] * product.price)
        cart[pid]['name'] = product.name  # 👈 ensure name is always there
        cart[pid]['price'] = float(product.price)  # 👈 refresh in case price changed
    else:
        cart[pid] = {
            "name": product.name,
            "quantity": quantity,
            "price": float(product.price),
            "subtotal": float(product.price * quantity),
        }

    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, f"{product.name} added to cart.")
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))



def cart_detail(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for pid, item in cart.items():
        product = Product.objects.get(id=pid)
        subtotal = product.price * item['quantity']
        total += subtotal
        items.append({
            
            'product': product,
            'quantity': item['quantity'],
            'subtotal': subtotal,
        })

    return render(request, 'frontend/shoping-cart.html', {'items': items, 'total': total})


def update_cart(request, product_id):
    if request.method == "POST":
        action = request.POST.get("action")
        quantity = request.POST.get("quantity")

        # ensure cart exists in session
        cart = request.session.get("cart", {})

        # convert product_id to string (since session keys are strings)
        pid = str(product_id)

        if pid not in cart:
            return HttpResponseBadRequest("Product not in cart")

        # Handle actions
        if action == "increase":
            cart[pid]["quantity"] += 1

        elif action == "decrease":
            cart[pid]["quantity"] = max(1, cart[pid]["quantity"] - 1)

        elif action == "update":
            try:
                new_qty = int(quantity)
                if new_qty > 0:
                    cart[pid]["quantity"] = new_qty
            except ValueError:
                pass

        elif action == "remove":
            cart.pop(pid, None)

        # Save back to session
        request.session["cart"] = cart
        request.session.modified = True
        messages.success(request, "Cart updated successfully!")
        return redirect("backend:cart_detail")   # change "cart" to your cart page name
    return HttpResponseBadRequest("Invalid request")

def remove_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, "Item removed from cart.")
    else:
        messages.warning(request, "Item not found in cart.")

    return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))


@login_required(login_url='backend:login_view')
def checkout(request):
    cart = request.session.get("cart", {})
    cart_items = []
    cart_total = 0
    cart_quantity_total = 0

    for product_id, item in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            name = product.name
            price = float(product.price)
        except Product.DoesNotExist:
            name = "Unknown Product"
            price = float(item.get("price", 0))

        quantity = int(item.get("quantity", 0))
        subtotal = quantity * price

        cart_quantity_total += quantity
        cart_total += subtotal

        cart_items.append({
            "id": product_id,
            "name": name,
            "quantity": quantity,
            "price": price,
            "subtotal": subtotal,
        })

    return render(request, "frontend/checkout.html", {
        "cart_items": cart_items,
        "cart_total": cart_total,
        "cart_quantity_total": cart_quantity_total,
    })


@login_required(login_url='backend:login_view')

def process_checkout(request):
    cart = request.session.get("cart", {})
    cart_items = list(cart.values())  # 👈 get the dict of items, not keys

    cart_quantity_total = sum(int(item["quantity"]) for item in cart_items)

    # ✅ block if less than 10
    if cart_quantity_total < 10:
        messages.warning(request, "You must order at least 10 items before checkout.")
        return redirect("frontend:checkout")

    if request.method == "POST":
        fullname = request.POST.get("fullname")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        # ⚡️ Save to DB or log later
        messages.success(request, "Your order has been placed successfully!")
        return redirect("frontend:checkout")

    return redirect("frontend:checkout")

