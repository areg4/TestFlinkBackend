from django.db import models
import uuid
# from .utils.ListField import ListField
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Company(models.Model):
    uuidCompany = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    nameCompany = models.CharField(max_length=50,blank=False,null=False)
    dscCompany = models.TextField(max_length=100,blank=False,null=False)
    tickerCompany = models.CharField(max_length=10, blank=False,null=False,unique=True)
    valCompany = ArrayField(models.FloatField())