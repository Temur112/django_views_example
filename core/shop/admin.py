from django.contrib import admin
from .models import Order, Product


class ProductInline(admin.TabularInline):
    model = Order.products.through
    extra = 1



class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    list_display = ('id', 'user', 'created_at', 'total')
    list_filter = ('id', 'user',)
    readonly_fields = ('id',)
    fieldsets = [
        ("Order options", {
            'fields': ('id', 'user',),
        })
    ]

    def queryset(self, request):
        return Order.objects.prefetch_related('products').prefetch_related('user')


    class Meta:
        model = Order


admin.site.register(Order, OrderAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price')
    list_display_links = ('id', 'name')


admin.site.register(Product, ProductAdmin)
