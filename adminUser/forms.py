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
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'rounded-full shadow-2xl w-full',
                'placeholder': 'Ingrese nombre'
            })
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
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'rounded-full shadow-2xl',
                'placeholder': 'Ingrese nombre'
            }),
            'timeExecute': forms.NumberInput(attrs={
                'class': 'rounded-full shadow-2xl text-center',
                'placeholder': 'Numero de horas'
            }),
            'area_redirect': forms.Select(
                attrs={
                    'class': 'rounded-full text-center',
                }
            )
        }

class CreateUserForm(forms.ModelForm):
    class Meta:
        model = CustumUser
        fields = ['username', 'first_name', 'last_name', 'email', 'area', 'permissions', 'is_staff', 'is_active']  # Incluye todos los campos necesarios
        labels = {
            'username': 'Nombre Usuario',
            'email': 'Correo Electronico',
            'is_staff': 'Otorgar Permisos de Administrador',
            'area': 'Área'
        }
        widgets = {
            'password': forms.PasswordInput(),
            'username': forms.TextInput(attrs={
                'class': 'rounded-md shadow-2xl w-full text-center text-xl',
                'placeholder': 'Username'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'rounded-md shadow-2xl w-full text-center text-xl',
                'placeholder': 'Nombre Asesor'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'rounded-md shadow-2xl w-full text-center text-xl',
                'placeholder': 'Apellido Asesor'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'rounded-md shadow-2xl w-full text-center text-xl',
                'placeholder': 'Correo Corporativo'
            }),
            'area': forms.Select(attrs={
                'class': 'rounded-md shadow-2xl w-full text-center text-xl',
            }),
            'permissions': forms.Select(attrs={
                'class': 'rounded-md shadow-2xl w-full text-center text-xl',
            }),
            'is_staff': forms.CheckboxInput(attrs={
                'class': 'cursor-pointer rounded-full w-[40px] h-[40px]',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'cursor-pointer rounded-full w-[40px] h-[40px]',
            }),
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