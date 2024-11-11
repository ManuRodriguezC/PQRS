from django import forms
from .models import PQRS

class PQRSCreateForm(forms.ModelForm):
    class Meta:
        model =  PQRS
        fields = ['asociado', 'typePQRS', 'description', 'file', 'image']
        
    def save(self, commit=True, user=None, *args, **kwargs):
        instance = super().save(commit=False)
        if user:
            instance.userCreated = user.username
        if commit:
            instance.save(*args, **kwargs)
        return instance