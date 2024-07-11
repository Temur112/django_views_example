from django.contrib import admin
from .models import Order, Product


class ProductInline(admin.TabularInline):
    model = Order.products.through
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    list_display = ("id", "user", "created_at", "total", "archived")
    list_display_links = ("id", "user")
    list_filter = ("id", "user", "archived")
    readonly_fields = ("id",)
    fieldsets = [
        (
            "Order options",
            {
                "fields": ("id", "user", "promo_code", "archived"),
            },
        )
    ]

    def queryset(self, request):
        return Order.objects.prefetch_related("products").prefetch_related("user")

    class Meta:
        model = Order


admin.site.register(Order, OrderAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "short_description", "price", "archived")
    list_display_links = ("id", "name")
    list_filter = ("archived",)

    def short_description(self, obj):
        if len(obj.description) < 40:
            return obj.description
        else:
            return obj.description[:40] + "..."


admin.site.register(Product, ProductAdmin)
