from frontend.models import *
def cart_item_count(request):
    cart = request.session.get('cart', {})
    count = sum(cart.values())

    cart_items = []
    if cart:
        product_ids = cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            cart_items.append({
                'product': product,
                'quantity': cart[str(product.id)],
                'total_price': product.price * cart[str(product.id)]
            })

    return {
        'cart_count': count,
        'cart_items': cart_items,
    }
