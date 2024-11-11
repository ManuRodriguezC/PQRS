from django.contrib import admin
from .models import *

@admin.register(PQRS)
class TypePQRSAdmin(admin.ModelAdmin):
    list_display = ['typePQRS', 'created', 'timeResponse', 'userCreated']