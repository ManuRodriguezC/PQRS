from .models import PQRS, Commets, Files, ResponsePQRS
from django.forms.models import inlineformset_factory
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from account.models import CustumUser
from adminUser.models import Areas
from django.conf import settings
from django import forms
from .utils import sendUserCreate, sendAsesorsCreate

class PQRSCreateForm(forms.ModelForm):
    class Meta:
        model =  PQRS
        fields = ['asociado', 'name', 'email', 'phone', 'typePQRS', 'description']
        labels = {
            'asociado': 'Numero de Documento',
            'name': 'Nombre Completo Asociado',
            'email': 'Correo Electronico',
            'phone': 'Numero de telefono',
            'typePQRS': 'Tipo de PQRS',
            'description': 'Descripción'
        }
        widgets = {
            'asociado': forms.NumberInput(attrs={
                'class': 'w-full rounded-md shadow-xl',
                'placeholder': 'Numero de Documento asociado'
            }),
            'name': forms.TextInput(attrs={
                'class': 'w-full rounded-md',
                'placeholder': 'Nombre Asociado'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full rounded-md',
                'placeholder': 'Correo Electronico'
            }),
            'phone': forms.NumberInput(attrs={
                'class': 'w-full rounded-md',
                'placeholder': 'Numero de Celular'
            }),
            'typePQRS': forms.Select(attrs={
                'class': 'w-full rounded-md',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full rounded-md',
                'rows': '4',
                'placeholder': 'Descriptión'
            }),
        }
        
    def save(self, commit=True, user=None, path=None, *args, **kwargs):
        instance = super().save(commit=False)
        if user:
            instance.userCreated = user.username

        if commit:
            instance.save(*args, **kwargs)

        allUsersArea = CustumUser.objects.filter(area=instance.typePQRS.area_redirect)
        emails = [user.email for user in allUsersArea]
        
        sendAsesorsCreate(instance.num, instance.typePQRS, emails)
        sendUserCreate(instance.typePQRS, instance.name, instance.num, instance.email)
        

        return instance

class PQRSUpdateForm(forms.ModelForm):
    class Meta:
        model = PQRS
        fields = ['asociado', 'name', 'email', 'phone']
        labels = {
            'asociado': 'Numero de Documento',
            'name': 'Nombre Completo Asociado',
            'email': 'Correo Electronico',
            'phone': 'Numero de telefono',
        }
        

class FileForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = ['file']
        labels = {
            'file': 'Archivo'
        }

FileFormSet = inlineformset_factory(
    PQRS, Files, form=FileForm, extra=0, can_delete=True
)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Commets
        fields = ['coment', 'file']
        labels = {
            'coment': 'Comentario',
            'file': 'Archivo'
        }
        widgets = {
            'coment': forms.Textarea(attrs={
                'class': 'rounded-md w-full',
                'rows': '3',
                'placeholder': 'Comentario o Respuesta'
            })
        }
    
    def save(self, commit=True, user=None, pqrs=None, *args, **kwargs):
        instance = super().save(commit=False)
        if user:
            instance.created_by = user.username
        if pqrs:
            instance.pqrs = pqrs
        if commit:
            instance.save(*args, **kwargs)
        return instance

class SearchForm(forms.Form):
    search = forms.CharField(label="", widget=forms.TextInput(attrs={
        'class': 'bg-gray-200 border-[10px] rounded-full',
        'placeholder': 'Buscar',
    }))

class ResponsePQRSForm(forms.ModelForm):
    class Meta:
        model = ResponsePQRS
        fields = ['response', 'file']
        labels = {
            'response': 'Respuesta al Asociado',
            'file': 'Adjuntar archivo'
        }
        widgets = {
            'response': forms.Textarea(attrs={
                'class': 'rounded-md w-full',
                'rows': '3',
                'placeholder': 'Comentario o Respuesta'
            })
        }
    
    def save(self, commit=True, user=None, pqrs=None, *args, **kwargs):
        instance = super().save(commit=False)
        if user:
            instance.response_by = user.username
        if pqrs:
            instance.pqrs = pqrs
        if commit:
            instance.save(*args, **kwargs)
        if pqrs:
            response = self.cleaned_data.get('response')
            file = self.cleaned_data.get('file')
            pqrs.waitingForResponse(response, file)
            pqrs.save()
        return instance

class ShareForm(forms.Form):
    typesAreas = forms.ChoiceField(label='Seleccione el área a compartir la PQRS')

    def __init__(self, areas, *args, **kwargs):
        areasList = areas.split(",")
        super().__init__(*args, **kwargs)

        types_area = Areas.objects.all()
        choices = [('', '-- Seleccione el área a compartir --')]
        choices += [(v.name, v.name) for v in types_area if v.name not in areasList]
        self.fields['typesAreas'].choices = choices

    def process(self, pqrs):
        """
        Método personalizado para procesar el formulario y modificar el objeto pqrs.
        """
        # Obtener el área seleccionada
        selected_area = self.cleaned_data.get('typesAreas')
        if selected_area:
            # Agregar el área seleccionada al atributo areas del objeto pqrs
            pqrs.areas += f",{selected_area}"
