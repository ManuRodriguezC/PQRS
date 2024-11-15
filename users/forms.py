from django import forms
from .models import PQRS, Commets, Files
from account.models import CustumUser
from django.core.mail import EmailMessage
from django.conf import settings
from django.forms.models import inlineformset_factory

class PQRSCreateForm(forms.ModelForm):
    class Meta:
        model =  PQRS
        fields = ['asociado', 'name', 'email', 'phone', 'typePQRS', 'description']
        
    def save(self, commit=True, user=None, *args, **kwargs):
        instance = super().save(commit=False)
        if user:
            instance.userCreated = user.username
        if commit:
            instance.save(*args, **kwargs)
        allUsersArea = CustumUser.objects.filter(area=instance.typePQRS.area_redirect)
        emails = [user.email for user in allUsersArea]
        message = f"Hola, se ha generado un PQRS de {instance.typePQRS}.\nPor favor revisa tu bandeja de PQRS para darle seguimiento."
        title = f"PQRS - {instance.typePQRS} a sido creada"
        email_message = EmailMessage(
            subject=title,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=emails
        )
        email_message.send()
        return instance


class FileForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = ['file']

FileFormSet = inlineformset_factory(
    PQRS, Files, form=FileForm, extra=0, can_delete=True
)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Commets
        fields = ['coment', 'file_add', 'image_add']
    
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
        'placeholder': 'Buscar'
    }))