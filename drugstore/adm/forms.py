from django import forms
from store.models import Produto

class ProductForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['name_product', 'description', 'price', 'image_product']