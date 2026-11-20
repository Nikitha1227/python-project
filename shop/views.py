from decimal import Decimal, ROUND_HALF_UP
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .cart import get_cart
from .models import Order, OrderItem, Product
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView

COUPONS = {
    "SAVE10": Decimal("0.10"),   # 10% percentage discount
    "TECH500": Decimal("500.00"), # Flat ₹500 discount
}


def _calculate_discount(subtotal: Decimal, code: str):
    code = (code or "").strip().upper()
    if code not in COUPONS:
        return "", Decimal("0.00"), subtotal

    rule = COUPONS[code]
    if rule < 1:
        discount = (subtotal * rule).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    else:
        discount = min(rule, subtotal)

    final_total = max(Decimal("0.00"), subtotal - discount)
    return code, discount, final_total


def product_list(request):
    products = Product.objects.filter(is_available=True, stock__gt=0)

    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    sort = request.GET.get("sort", "")
    if sort == "price_asc":
        products = products.order_by("price")
    elif sort == "price_desc":
        products = products.order_by("-price")
    else:
        products = products.order_by("-created_at")

    return render(request, "shop/product_list.html", {
        "products": products,
        "query": query,
        "sort": sort,
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_available=True)
    return render(request, "shop/product_detail.html", {"product": product})


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_available=True)
    cart = request.session.get("shopping_cart", {})
    key = str(product.id)
    current_qty = cart.get(key, 0)

    try:
        add_qty = max(1, int(request.POST.get("quantity", 1)))
    except ValueError:
        add_qty = 1

    if current_qty + add_qty > product.stock:
        messages.warning(request, f"Only {product.stock} in stock for {product.name}.")
    else:
        cart[key] = current_qty + add_qty
        request.session["shopping_cart"] = cart
        messages.success(request, f"Added {add_qty} × '{product.name}' to your cart!")

    return redirect("shop:product_list")


def cart_detail(request):
    items, subtotal = get_cart(request)
    applied_code = request.session.get("coupon_code", "")
    code, discount, final_total = _calculate_discount(subtotal, applied_code)
    if applied_code and not code:
        request.session.pop("coupon_code", None)

    return render(request, "shop/cart_detail.html", {
        "items": items,
        "subtotal": subtotal,
        "coupon_code": code,
        "discount": discount,
        "total": final_total,
    })


@require_POST
def apply_coupon(request):
    code = request.POST.get("coupon_code", "").strip().upper()
    if not code:
        request.session.pop("coupon_code", None)
        messages.info(request, "Coupon code removed.")
    elif code in COUPONS:
        request.session["coupon_code"] = code
        messages.success(request, f"Promo code '{code}' applied!")
    else:
        messages.warning(request, f"Invalid code '{code}'. Try SAVE10 or TECH500.")
    return redirect("shop:cart_detail")


@require_POST
def cart_update(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_available=True)
    cart = request.session.get("shopping_cart", {})
    key = str(product.id)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except ValueError:
        quantity = 1

    if quantity <= 0:
        cart.pop(key, None)
    elif quantity > product.stock:
        cart[key] = product.stock
        messages.warning(request, f"Only {product.stock} available for {product.name}.")
    else:
        cart[key] = quantity

    request.session["shopping_cart"] = cart
    return redirect("shop:cart_detail")


@require_POST
def cart_remove(request, product_id):
    cart = request.session.get("shopping_cart", {})
    cart.pop(str(product_id), None)
    request.session["shopping_cart"] = cart
    return redirect("shop:cart_detail")


@require_POST
def checkout(request):
    items, subtotal = get_cart(request)
    if not items:
        messages.warning(request, "Your cart is empty.")
        return redirect("shop:product_list")

    for item in items:
        product = item["product"]
        if item["quantity"] > product.stock:
            messages.warning(
                request,
                f"Not enough stock for {product.name} (only {product.stock} left)."
            )
            return redirect("shop:cart_detail")

    code, discount, final_total = _calculate_discount(
        subtotal, request.session.get("coupon_code", "")
    )
    full_name = request.POST.get("full_name", "").strip()
    address = request.POST.get("address", "").strip()

    order = Order.objects.create(
        full_name=full_name or "Customer",
        address=address or "Store Pickup",
        coupon_code=code,
        discount_amount=discount,
        total_paid=final_total,
    )

    for item in items:
        product = item["product"]
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item["quantity"],
            unit_price=product.price,
        )
        product.stock -= item["quantity"]
        if product.stock == 0:
            product.is_available = False
        product.save()

    request.session.pop("shopping_cart", None)
    request.session.pop("coupon_code", None)
    messages.success(request, f"Order #{order.id} confirmed!")
    return redirect("shop:order_receipt", order_id=order.id)


def order_receipt(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "shop/order_receipt.html", {"order": order})

def order_history(request):
    orders = Order.objects.prefetch_related("items__product").order_by("-created_at")
    return render(request, "shop/order_history.html", {"orders": orders})


def receipts_list(request):
    orders = Order.objects.prefetch_related("items__product").order_by("-created_at")
    return render(request, "shop/receipts_list.html", {"orders": orders})


def account_details(request):
    if request.user.is_authenticated and request.method == "POST":
        request.user.first_name = request.POST.get("first_name", "").strip()
        request.user.last_name = request.POST.get("last_name", "").strip()
        request.user.email = request.POST.get("email", "").strip()
        request.user.save()
        messages.success(request, "Account details updated!")
        return redirect("shop:account_details")

    orders = Order.objects.all()
    total_orders = orders.count()
    total_spent = sum((o.total_paid for o in orders), Decimal("0.00"))
    last_order = orders.order_by("-created_at").first()

    return render(request, "shop/account_details.html", {
        "user": request.user,
        "total_orders": total_orders,
        "total_spent": total_spent,
        "last_order": last_order,
    })
class StoreLoginView(LoginView):
    template_name = "shop/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Welcome back, {self.request.user.get_username()}!")
        return response


class StoreLogoutView(LogoutView):
    next_page = "shop:product_list"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You have been signed out.")
        return super().dispatch(request, *args, **kwargs)


def register(request):
    if request.user.is_authenticated:
        return redirect("shop:product_list")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created! Welcome to TechCart, {user.username}.")
            return redirect("shop:product_list")
    else:
        form = UserCreationForm()

    return render(request, "shop/register.html", {"form": form})