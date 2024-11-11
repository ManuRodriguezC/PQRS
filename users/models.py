from django.db import models
from adminUser.models import *
from datetime import timedelta, datetime
from django.utils import timezone

class PQRSManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        
        for pqrs in queryset:
            pqrs.check_time_response()
        return queryset

class PQRS(models.Model):
    """"""
    typePQRS = models.ForeignKey(TypesPQRS, on_delete=models.CASCADE)
    asociado = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=1000)
    file = models.FileField(upload_to='files/', null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    timeResponse = models.DateTimeField(null=True, blank=True)
    userCreated = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default="Open")
    
    objects = PQRSManager()
    
    def save(self, *args, **kwargs):
        if self.typePQRS and not self.timeResponse:
            dateEnd = datetime.now() + timedelta(hours=self.typePQRS.timeExecute)
            self.timeResponse = dateEnd
        super(PQRS, self).save(*args, **kwargs)
    
    def check_time_response(self):
        if self.timeResponse and self.timeResponse < timezone.now() and self.status == "Open":
            self.status = "Expired"
            self.save()
    
    class Meta:
        ordering = ['-created']
