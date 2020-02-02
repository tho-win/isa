from django.db import models

# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=300)
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    pass

class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    swiper = models.BooleanField(default=False)
    schools = models.ManyToManyField(School)