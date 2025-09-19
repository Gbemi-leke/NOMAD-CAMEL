from frontend.models import *
from backend.models import *


def cart_item_count(request):
    cart = request.session.get('cart', {})

    count = sum(item['quantity'] for item in cart.values())

    cart_items = []
    grand_total = 0

    if cart:
        product_ids = cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            quantity = cart[str(product.id)]['quantity']
            total_price = product.price * quantity
            grand_total += total_price
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': total_price
            })

    return {
        'cart_count': count,
        'cart_items': cart_items,
        'cart_total': grand_total,   
    }


def wishlist_count(request):
    if request.user.is_authenticated:
        return {
            "wishlist_count": Wishlist.objects.filter(user=request.user).count()
        }
    return {"wishlist_count": 0}