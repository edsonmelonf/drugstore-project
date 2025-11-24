from django import forms

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=200)
    address = forms.CharField(max_length=300)


    PAYMENT_CHOICES = [
        ('pix', 'Pix'),
        ('card', 'Cartão'),
        ('cash', 'Dinheiro'),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect, 
        label="Forma de pagamento"
    )
