from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .models import Product, Order


def index(request):
    return render(request, 'shop/base.html')


class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(archived=False)


class CreateProductView(CreateView):
    model = Product
    template_name = 'shop/create_product.html'
    fields = ['name', 'price', 'description', 'discount']
    success_url = reverse_lazy("shop:products")


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.archived:
            raise Http404("This product is archived. Thus it can't be displayed to you !")
        return obj


class UpdateProductView(UpdateView):
    model = Product
    # context_object_name = 'product'
    template_name_suffix = "_update"
    fields = ["name", "price", "description", "discount"]

    def get_success_url(self):
        return reverse("shop:productDetails", kwargs={"pk": self.object.pk})


class DeleteProductView(DeleteView):
    model = Product
    template_name = "shop/product_delete_confirm.html"
    success_url = reverse_lazy("shop:products")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrdersListView(ListView):
    model = Order
    context_object_name = 'orders'
    queryset = Order.objects.prefetch_related('products').prefetch_related('user').filter(archived=False)


class CreateOrderView(CreateView):
    model = Order
    template_name = 'shop/create_order.html'
    fields = ['delivery_address', 'user', 'promo_code', 'products']
    success_url = reverse_lazy("shop:orders")


class OrdersDetailView(DetailView):
    model = Order
    template_name = 'shop/order_detail.html'
    context_object_name = 'order'
    queryset = Order.objects.prefetch_related('products').prefetch_related('user')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.archived:
            raise Http404("This order is archived. Thus it can't be displayed to you !")
        return obj


class UpdateOrder(UpdateView):
    model = Order
    template_name = 'shop/update_order.html'
    fields = ['delivery_address', 'user', 'promo_code', 'products']

    def get_success_url(self):
        return reverse("shop:ordersDetails", kwargs={"pk": self.object.pk})


class DeleteOrderView(DeleteView):
    model = Order
    template_name = "shop/delete_order_confirm.html"
    success_url = reverse_lazy("shop:orders")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)

