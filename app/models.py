from django.db import models

# Create your models here.

class Connection(models.Model):
    host = models.CharField(max_length=40)
    user = models.CharField(max_length=20)
    password = models.CharField(max_length=15)