from django.db import models
from django.contrib.auth.models import AbstractUser
from adminUser.models import Areas

class CustumUser(AbstractUser):
    area = models.ForeignKey(Areas, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.username
