from django import forms
from store.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name_product', 'description', 'price', 'image_product']