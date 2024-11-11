from django.db import models

class Areas(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

class TypesPQRS(models.Model):
    name = models.CharField(max_length=100)
    timeExecute = models.IntegerField()
    area_redirect = models.ForeignKey(Areas, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def timeResponse(self):
        return self.timeExecute