from .models import TypesPQRS, Areas
from django import forms

from account.models import CustumUser

class AreasForms(forms.ModelForm):
    class Meta:
        model = Areas
        fields = '__all__'
        labels = {
            'name': 'Nombre de la Area Nueva'
        }

class TypesPQRSForms(forms.ModelForm):
    class Meta:
        model = TypesPQRS
        fields = '__all__'
        labels = {
            'name': 'Nombre PQRS',
            'timeExecute': 'Tiempo maximo de Respuesta en horas',
            'area_redirect': 'Area a la que se redirigira la PQRS'
        }

class CreateUserForm(forms.ModelForm):
    class Meta:
        model = CustumUser
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'area']  # Incluye todos los campos necesarios
        labels = {
            'username': 'Nombre Usuario',
            'email': 'Correo Electronico',
            'is_staff': 'Otorgar Permisos de Administrador',
            'area': 'Área'
        }
        widgets = {
            'password': forms.PasswordInput(),  # Para que el campo de contraseña sea tipo password
        }
        help_texts = {
            'username': '',
            'email': 'Ingrese el correo Corporativo',
            'is_staff': 'Si otorga los permisos, el usuario podra crear y redirigir PQRS de forma manual'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields.pop('is_active')