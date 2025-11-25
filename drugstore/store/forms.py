from django import forms
from .models import Produto

class AdicionarEstoqueForm(forms.Form):
    produto = forms.ModelChoiceField(queryset=Produto.objects.all(), label="Produto")
    quantidade = forms.IntegerField(min_value=1, label="Quantidade")
