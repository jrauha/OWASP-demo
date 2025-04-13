from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Product, Order, PasswordReset
from django.db import transaction
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


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
            # Demo: OWASP A04:2021 – Insecure Design
            # The total price is read from the request instead of being calculated
            # based on the product price and quantity. This allows users to manipulate
            # the total price during checkout.
            # Fix:
            # total_price = product.price * quantity
            total_price = float(request.POST.get("total_price", 0))
            customer_request = request.POST.get("customer_request", "")
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
                customer_request=customer_request,
                total_price=total_price,
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


# Password reset views
# Simple password reset functionality to demonstrate common
# vulnerabilities and their fixes.


def password_reset(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            token = PasswordReset(user=user)
            token.save()
            reset_link = request.build_absolute_uri(
                f"/reset/{token.user.id}/{token.token}/"
            )
            send_mail(
                subject="Password Reset Request",
                message=f"Click the link to reset your password: {reset_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
            return redirect("password_reset_done")
        else:
            # Demo: A05:2021 - Security Misconfiguration
            # Application leaks information about whether the email exists
            # in the system. This can be exploited by attackers to enumerate
            # valid email addresses.
            # Fix:
            # Do not disclose whether the email exists or not.
            return HttpResponse("Email not found", status=404)

    return render(request, "password_reset.html")


def password_reset_done(request):
    return render(request, "password_reset_done.html")


def password_reset_confirm(request, uid, token):
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        with transaction.atomic():
            reset = PasswordReset.objects.filter(user_id=uid, token=token).first()

            if reset:
                # Demo: OWASP A07:2021 – Identification and Authentication Failures
                # The token is not validated for expiration.
                # Fix:
                # Implement token expiration logic here
                # Example: Check if the token is older than a certain threshold
                # if timezone.now() - reset.created_at > timedelta(hours=1):
                #     return HttpResponse("Token expired", status=400)

                user = reset.user
                # Demo: A07:2021 - Identification and Authentication Failures
                # The password is not validated for strength or complexity.
                # Fix:
                # Implement password validation logic here
                user.set_password(new_password)
                user.save()
                reset.delete()
                return redirect("password_reset_complete")
    return render(request, "password_reset_confirm.html", {"uid": uid, "token": token})


def password_reset_complete(request):
    return render(request, "password_reset_complete.html")
