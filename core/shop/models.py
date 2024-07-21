from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.signals import m2m_changed


def create_preview_path(instance, filename):
    return "products/product_{pk}/preview/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class Product(models.Model):
    '''model for create product'''
    name = models.CharField(max_length=100, blank=False, db_index=True)
    description = models.TextField(blank=True, null=False, db_index=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    preview = models.ImageField(null=True, blank=True, upload_to=create_preview_path)

    def __str__(self):
        return self.name


def product_image_path(instance, filename):
    return "products/product_{pk}/images/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to=product_image_path)
    description = models.TextField(blank=True, null=False)

    def __str__(self):
        return self.product.name


class Order(models.Model):
    delivery_address = models.CharField(max_length=100, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name="products")
    _total = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    promo_code = models.CharField(max_length=20, blank=True, null=False)
    archived = models.BooleanField(default=False)
    receipt = models.FileField(null=True, upload_to="orders/receipts")

    @property
    def total(self):
        return self._total


def update_order_totals(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        instance._total += instance.products.aggregate(total=Sum("price"))["total"]
        instance.save()


m2m_changed.connect(update_order_totals, sender=Order.products.through)
