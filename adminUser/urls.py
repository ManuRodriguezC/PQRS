from django.urls import path
from .views import *

urlpatterns = [
    path('', areasAll, name="areas"),
    path('deleteArea/<int:id>/', deleteArea, name="deleteArea"),
    path('tiposPQRS/', typesPQRSAll, name="typesPQRS"),
    path('deleteTypePQRS/<int:id>/', deleteTypePQRS, name="deleteTypePQRS"),
    path('users/', users, name="users")
]