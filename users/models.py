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
    num = models.CharField(max_length=20)
    typePQRS = models.ForeignKey(TypesPQRS, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    asociado = models.IntegerField(null=True, blank=True)
    email = models.EmailField()
    phone = models.IntegerField()
    description = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    timeResponse = models.DateTimeField(null=True, blank=True)
    userCreated = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default="Open")
    close_by = models.CharField(max_length=100, null=True, blank=True)
    closed = models.DateTimeField(null=True, blank=True)

    objects = PQRSManager()

    def save(self, *args, **kwargs):
        if self.typePQRS and not self.timeResponse:
            dateEnd = datetime.now() + timedelta(hours=self.typePQRS.timeExecute)
            self.timeResponse = timezone.make_aware(dateEnd, timezone.get_current_timezone())
        
        if not self.num:
            super().save(*args, **kwargs)
            self.num = f"CTT10{str(self.id).rjust(7, '0')}"
            kwargs['force_insert'] = False
        super(PQRS, self).save(*args, **kwargs)

    def check_time_response(self):
        if self.timeResponse and self.timeResponse < timezone.now() and self.status == "Open":
            self.status = "Expired"
            self.save()

    def closePQRS(self, user, *args, **kwargs):
        self.status = "Close"
        self.close_by = user
        self.closed = datetime.now()
        super(PQRS, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created']

class Files(models.Model):
    """"""
    pqrs = models.ForeignKey(PQRS, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(null=True, blank=True, upload_to='files/')
    created = models.DateTimeField(auto_now_add=True)
    
    def nameFile(self):
        if self.file:
            return self.file.name.split('/')[-1]
        return None

class Commets(models.Model):
    """"""
    pqrs = models.ForeignKey(PQRS, on_delete=models.SET_NULL, null=True, blank=True)
    coment = models.CharField(max_length=1000)
    file = models.FileField(null=True, blank=True, upload_to='files/')
    created_by = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    
    def nameFile(self):
        if self.file:
            return self.file.name.split('/')[-1]
        return None
