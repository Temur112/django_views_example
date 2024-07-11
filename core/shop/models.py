from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.signals import m2m_changed


# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True, null=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    delivery_address = models.CharField(max_length=100, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name='products')
    _total = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    promo_code = models.CharField(max_length=20, blank=True, null=False)
    archived = models.BooleanField(default=False)

    @property
    def total(self):
        return self._total


def update_order_totals(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance._total += instance.products.aggregate(total = Sum('price'))['total']
        instance.save()


m2m_changed.connect(update_order_totals, sender=Order.products.through)