from django.contrib import admin
from .models import *

@admin.register(PQRS)
class TypePQRSAdmin(admin.ModelAdmin):
    list_display = ['num', 'typePQRS', 'timeResponse', 'status']

@admin.register(Commets)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['pqrs', 'coment', 'created_by']

@admin.register(Files)
class FilesAdmin(admin.ModelAdmin):
    list_display = ['pqrs', 'file', 'created']
    
@admin.register(ResponsePQRS)
class ResponsesPQRSAdmin(admin.ModelAdmin):
    list_display = ['pqrs', 'file', 'response']