from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("product/<int:product_id>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/coupon/", views.apply_coupon, name="apply_coupon"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/update/<int:product_id>/", views.cart_update, name="cart_update"),
    path("cart/remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("checkout/", views.checkout, name="checkout"),
    path("order/<int:order_id>/", views.order_receipt, name="order_receipt"),
    path("orders/", views.order_history, name="order_history"),
    path("receipts/", views.receipts_list, name="receipts_list"),
    path("account/", views.account_details, name="account_details"),
    path("login/", views.StoreLoginView.as_view(), name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.StoreLogoutView.as_view(), name="logout"),
]