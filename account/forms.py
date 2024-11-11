from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustumUser

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Nombre de Usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    
