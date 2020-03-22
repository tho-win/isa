from django.db import models

class DummyUser(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    computing_id = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    bio = models.TextField(max_length=500, blank=True)
    password = models.CharField(max_length=100, default="")
