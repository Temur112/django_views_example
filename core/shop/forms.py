from django import forms

from shop.models import Product


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        one_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [one_file_clean(d, initial) for d in data]
        else:
            result = one_file_clean(data, initial)
        return result


class ProductForm(forms.ModelForm):
    product_images = MultipleFileField(required=False)

    class Meta:
        model = Product
        fields = ["name", "price", "description", "discount", "preview"]
