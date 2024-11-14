from django.contrib import admin
from .models import *

@admin.register(PQRS)
class TypePQRSAdmin(admin.ModelAdmin):
    list_display = ['typePQRS', 'created', 'timeResponse', 'userCreated']

@admin.register(Commets)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['pqrs', 'coment', 'created_by']