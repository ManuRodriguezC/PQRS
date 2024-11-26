from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustumUser

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Nombre de Usuario', widget=forms.TextInput(attrs={
        'class': 'rounded-full w-full text-black',
        'placeholder': 'Nombre Usuario'
    }))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={
        'class': 'rounded-full w-full text-black',
        'placeholder': 'Contraseña'
    }))
    

