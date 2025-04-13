from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from webshop.models import Product, Order


class Command(BaseCommand):
    help = "Creates demo users, products, and orders."

    def handle(self, *args, **options):
        # Create demo users
        user1, _ = User.objects.get_or_create(
            username="demo_user1", defaults={"email": "demo1@example.com"}
        )
        user1.set_password("demo1pass")
        user1.save()

        user2, _ = User.objects.get_or_create(
            username="demo_user2", defaults={"email": "demo2@example.com"}
        )
        user2.set_password("demo2pass")
        user2.save()

        user3, _ = User.objects.get_or_create(
            username="demo_user3", defaults={"email": "demo3@example.com"}
        )
        user3.set_password("demo3pass")
        user3.save()

        # Create demo flight tickets
        product1, _ = Product.objects.get_or_create(
            name="Flight to New York",
            defaults={
                "price": 299.99,
                "description": "One-way ticket to New York",
                "stock": 50,
                "departure_date": "2025-05-01T10:00:00Z",
                "departure_location": "Los Angeles",
                "destination": "New York",
            },
        )
        product2, _ = Product.objects.get_or_create(
            name="Flight to London",
            defaults={
                "price": 499.99,
                "description": "Round-trip ticket to London",
                "stock": 30,
                "departure_date": "2025-06-15T15:00:00Z",
                "departure_location": "New York",
                "destination": "London",
            },
        )
        product3, _ = Product.objects.get_or_create(
            name="Flight to Tokyo",
            defaults={
                "price": 799.99,
                "description": "One-way ticket to Tokyo",
                "stock": 20,
                "departure_date": "2025-07-20T20:00:00Z",
                "departure_location": "San Francisco",
                "destination": "Tokyo",
            },
        )

        # Create demo orders
        order1, _ = Order.objects.get_or_create(
            user=user1, product=product1, quantity=2, total_price=product1.price * 2
        )
        order1.save()

        order2, _ = Order.objects.get_or_create(
            user=user2, product=product3, quantity=1, total_price=product3.price * 1
        )
        order2.save()

        self.stdout.write("Demo data initialized successfully.")
