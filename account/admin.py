from django.contrib import admin
from .models import *

@admin.register(CustumUser)
class CustumUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'area')