from django.db import models
from adminUser.models import *
from datetime import timedelta, datetime
from adminUser.models import TypesPQRS
from django.utils import timezone
import uuid
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

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
    areas = models.CharField(max_length=1000, null=True, blank=True)
    name = models.CharField(max_length=200)
    asociado = models.IntegerField()
    email = models.EmailField()
    phone = models.IntegerField()
    description = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    timeResponse = models.DateTimeField(null=True, blank=True)
    userCreated = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default="Open")
    close_by = models.CharField(max_length=100, null=True, blank=True)
    closed = models.DateTimeField(null=True, blank=True)
    dateResponse = models.DateTimeField(null=True, blank=True)
    tokenControl = models.CharField(max_length=100, null=True, blank=True)

    objects = PQRSManager()

    def save(self, *args, **kwargs):
        if self.typePQRS and not self.timeResponse:
            dateEnd = datetime.now() + timedelta(hours=self.typePQRS.timeExecute)
            self.timeResponse = timezone.make_aware(dateEnd, timezone.get_current_timezone())
            name_pqrs = self.typePQRS.area_redirect
            setName = str(name_pqrs)
            self.areas = setName
        
        if not self.num:
            super().save(*args, **kwargs)
            self.num = f"CTT10{str(self.id).rjust(7, '0')}"
            kwargs['force_insert'] = False
        super(PQRS, self).save(*args, **kwargs)

    def check_time_response(self):
        if self.timeResponse and self.timeResponse < timezone.now() and self.status == "Open":
            self.status = "Expired"
            self.closed = timezone.now()
            self.save()
        if self.dateResponse and self.dateResponse < timezone.now() and self.status == "Wait":
            self.status = "Close"
            self.closed = timezone.now()
            self.save()

    def closePQRS(self, user, *args, **kwargs):
        self.status = "Close"
        self.close_by = user
        self.closed = datetime.now()
        super(PQRS, self).save(*args, **kwargs)
    
    def closedForUser(self, *args, **kwargs):
        self.status = "CloseForUser"
        self.closed = datetime.now()
        super(PQRS, self).save(*args, **kwargs)
    
    def waitingForResponse(self, response, file):
        dateForResponse = datetime.now() + timedelta(hours=720)
        self.dateResponse = dateForResponse
        self.status = "Wait"
        token = uuid.uuid4()
        self.tokenControl = token
        num = self.num
        email = self.email
        
        html_message = render_to_string('emails/sendResponse.html', {
            'name': self.name,
            'type': self.typePQRS,
            'response': response,
            'si': f"http://127.0.0.1:8000/solicitud-pqrs/{num}/{token}/",
            'no': f"http://127.0.0.1:8000/solicitud-finalizada-sin-exito/{num}/{token}/"
        })
        
        email_message = EmailMessage(
            f'Respuesta Solicitud {self.typePQRS}',
            html_message,
            settings.EMAIL_HOST_USER,
            to=[email],
            )
        if file:
            email_message.attach(file.name, file.read(), file.content_type)

        email_message.content_subtype = 'html'
        email_message.send()

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

class ResponsePQRS(models.Model):
    pqrs = models.ForeignKey(PQRS, on_delete=models.SET_NULL, null=True, blank=True)
    response = models.CharField(max_length=1000)
    response_by = models.CharField(max_length=200)
    file = models.FileField(null=True, blank=True, upload_to='files/responses')
    date = models.DateTimeField(auto_now_add=True)