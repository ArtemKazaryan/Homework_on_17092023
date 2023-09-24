from django.forms import ModelForm
from .models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ['slug', 'created', 'updated']
        readonly_fields = ['available']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

