from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Product, Order
from django.db import transaction
from django.contrib.auth.models import User


def product_list(request):
    products = Product.objects.all()

    return render(request, "product_list.html", {"products": products})


@login_required
def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    if not product:
        return HttpResponse("Product not found", status=404)

    return render(request, "product_detail.html", {"product": product})


@login_required
def checkout(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))
        product = Product.objects.get(id=product_id)
        if not product:
            return HttpResponse("Product not found", status=404)
        request.session["cart_product_quantity"] = quantity
        request.session["cart_product_id"] = product.id
        return render(
            request,
            "checkout.html",
            {
                "cart_items": [
                    {
                        "product": product,
                        "quantity": quantity,
                    }
                ],
                "total_price": product.price * quantity,
                "quantity": quantity,
            },
        )
    else:
        return render(request, "checkout.html")


@login_required
def process_checkout(request):
    if request.method == "POST":
        with transaction.atomic():
            product_id = request.session.get("cart_product_id")
            quantity = request.session.get("cart_product_quantity", 1)
            product = Product.objects.get(id=product_id)

            if not product:
                return HttpResponse("Product not found", status=404)
            if product.stock < int(quantity):
                return HttpResponse("Not enough stock available", status=400)

            product.stock -= int(quantity)
            product.save()

            order = Order(
                user=request.user,
                product=product,
                quantity=int(quantity),
            )
            order.save()

            del request.session["cart_product_id"]
            del request.session["cart_product_quantity"]
        return redirect("profile", user_id=request.user.id)
    else:
        return redirect("product_list")


@login_required
def profile(request, user_id=None):
    # OWASP A01:2021 - Broken Access Control
    # User ID should be obtained from the request.user object
    # to prevent unauthorized access to other users' profiles.
    # Fix:
    # user_id = request.user.id
    user = User.objects.get(id=user_id)
    orders = Order.objects.filter(user=user)
    return render(request, "profile.html", {"profile": user, "orders": orders})
