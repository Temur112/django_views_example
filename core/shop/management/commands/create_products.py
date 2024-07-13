from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shop.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        product_titles = [
            "Tv", "CellPhone", "Phone", "Smartphone", "Notebook", "Laptop"
        ]
        user = User.objects.get(username='admin')
        self.stdout.write("Creating products...")
        for product_title in product_titles:
            product, status = Product.objects.get_or_create(name=product_title, created_by=user)
            self.stdout.write(f"Created product {product_title} and status: {status}")

        self.stdout.write(self.style.SUCCESS("Successfully created products."))
