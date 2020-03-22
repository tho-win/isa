from django.db import models

class DummyUser(models.Model):
    email = models.EmailField(unique=True, default="")
    username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    computing_id = models.CharField(max_length=10, default="")
    phone_number = models.CharField(max_length=20, blank=True)
    bio = models.TextField(max_length=500, blank=True)
