from django.db import models
from django.contrib.auth.models import AbstractUser
from adminUser.models import Areas

TYPES_USERS = [
    ('superadmin', 'superadmin'),
    ('coordinador', 'coordinador'),
    ('usuario', 'usuario'),
]

class CustumUser(AbstractUser):
    area = models.ForeignKey(Areas, on_delete=models.SET_NULL, null=True, blank=True)
    permissions = models.CharField(choices=TYPES_USERS, max_length=100)
    
    def __str__(self):
        return self.username
    
    def currentArea(self):
        return self.area

    def coordinador(self):
        return self.permissions == "coordinador"