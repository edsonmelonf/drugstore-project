from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm (UserCreationForm):
    email = forms.EmailField()

    
    class Meta:
        model = User
        fields = ['email', 'password1','password2']


    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data['email']

        user.email = email
        user.username = email  

        if commit:
            user.save()

        return user
