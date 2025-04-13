import random
from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    product_type = models.CharField(max_length=50, default="ticket")
    departure_date = models.DateTimeField(null=True, blank=True)
    departure_location = models.CharField(max_length=255, null=True, blank=True)
    destination = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    customer_request = models.TextField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()

        super().save(*args, **kwargs)

    def generate_token(self):
        # Demo: OWASP A07:2021 – Identification and Authentication Failures
        # Token is a random 5-digit number. This value is trivial to guess
        # using brute force.
        # Fix: Use a secure random token generator.
        # Example: Use Django's built-in token generator
        # from django.utils.crypto import get_random_string
        # return get_random_string(length=32)
        return str(random.randint(0, 1000)).zfill(5)

    def __str__(self):
        return f"Password reset for {self.user.username}"
