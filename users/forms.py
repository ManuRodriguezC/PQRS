from django import forms
from .models import PQRS, Commets

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
        print(instance)
        print(instance.typePQRS)
        return instance

class CommentForm(forms.ModelForm):
    class Meta:
        model = Commets
        fields = ['coment']
    
    def save(self, commit=True, user=None, pqrs=None, *args, **kwargs):
        instance = super().save(commit=False)
        if user:
            instance.created_by = user.username
        if pqrs:
            instance.pqrs = pqrs
        if commit:
            instance.save(*args, **kwargs)
        return instance