from django.contrib import admin
from .models import Areas, TypesPQRS

@admin.register(Areas)
class AreasAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(TypesPQRS)
class TypePQRSAdmin(admin.ModelAdmin):
    list_display = ['name', 'timeExecute', 'area_redirect']
