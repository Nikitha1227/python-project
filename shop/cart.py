from decimal import Decimal
from .models import Product


def get_cart(request):
    cart = request.session.get("shopping_cart", {})
    product_ids = [int(pid) for pid in cart.keys()]
    products = Product.objects.filter(id__in=product_ids)
    product_map = {p.id: p for p in products}

    items = []
    total = Decimal("0.00")

    for pid_str, quantity in cart.items():
        product = product_map.get(int(pid_str))
        if not product:
            continue
        qty = int(quantity)
        line_total = product.price * qty
        total += line_total
        items.append({
            "product": product,
            "quantity": qty,
            "line_total": line_total,
        })

    return items, total