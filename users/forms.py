from django import forms
from .models import PQRS, Commets, Files, ResponsePQRS
from account.models import CustumUser
from django.core.mail import EmailMessage
from django.conf import settings
from django.forms.models import inlineformset_factory
from django.template.loader import render_to_string
from adminUser.models import Areas

class PQRSCreateForm(forms.ModelForm):
    class Meta:
        model =  PQRS
        fields = ['asociado', 'name', 'email', 'phone', 'description', 'typePQRS']
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
            instance.areas = user.area
        if commit:
            instance.save(*args, **kwargs)
        allUsersArea = CustumUser.objects.filter(area=instance.typePQRS.area_redirect)
        
        emails = [user.email for user in allUsersArea]
        
        url = f"http://127.0.0.1:8000/pqrs/{instance.num}"
        
        html_message = render_to_string('emails/createpqrs.html', {
            'pqrs': instance.typePQRS,
            'url': url
        })
        
        # messageText = f"""
        #     Hola, se ha generado una PQRS de {instance.typePQRS}.\n
        #     Por favor revise su bandeja en PQRS abiertas para darle seguimiento,
        #     o ingrese al siguiente link: {url}
        # """
        # message = messageText
        # title = f"PQRS - {instance.typePQRS} a sido creada"
        
        email_message = EmailMessage(
            f"PQRS Generada - {instance.typePQRS}",
            html_message,
            settings.EMAIL_HOST_USER,
            emails
        )
        email_message.content_subtype = 'html'
        
        email_message.send()
        return instance


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