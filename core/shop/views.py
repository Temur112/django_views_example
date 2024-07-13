from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from .models import Product, Order


def index(request):
    return render(request, "shop/base.html")


class ProductListView(ListView):
    model = Product
    template_name = "shop/product_list.html"
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)


class CreateProductView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "shop.add_product"
    login_url = "/accounts/login/"

    permission_denied_message = "You do not have enough privileges to create a new product."
    model = Product
    template_name = "shop/create_product.html"
    fields = ["name", "price", "description", "discount"]
    success_url = reverse_lazy("shop:products")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductDetailView(DetailView):
    model = Product
    template_name = "shop/product_detail.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.archived:
            raise Http404(
                "This product is archived. Thus it can't be displayed to you !"
            )
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_object = self.get_object()
        user = self.request.user

        context["has_permission"] = user.has_perms(["shop.change_product",]) or user.is_superuser or my_object.created_by == user
        return context


class UpdateProductView(UserPassesTestMixin, UpdateView):
    model = Product
    # context_object_name = 'product'
    template_name_suffix = "_update"
    fields = ["name", "price", "description", "discount"]

    def get_success_url(self):
        return reverse("shop:productDetails", kwargs={"pk": self.object.pk})

    def test_func(self):
        user = self.request.user
        my_object = self.get_object()
        return user.has_perms(["shop.change_product",]) or user.is_superuser or my_object.created_by == user


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
    context_object_name = "orders"
    queryset = (
        Order.objects.prefetch_related("products")
        .prefetch_related("user")
        .filter(archived=False)
    )


class CreateOrderView(CreateView):
    model = Order
    template_name = "shop/create_order.html"
    fields = ["delivery_address", "user", "promo_code", "products"]
    success_url = reverse_lazy("shop:orders")


class OrdersDetailView(DetailView):
    model = Order
    template_name = "shop/order_detail.html"
    context_object_name = "order"
    queryset = Order.objects.prefetch_related("products").prefetch_related("user")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.archived:
            raise Http404("This order is archived. Thus it can't be displayed to you !")
        return obj


class UpdateOrder(UpdateView):
    model = Order
    template_name = "shop/update_order.html"
    fields = ["delivery_address", "user", "promo_code", "products"]

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
