from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    password = models.CharField(max_length=100, default="password")
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    bio = models.TextField(max_length=100, blank=True)
    date_joined = models.DateTimeField(default=timezone.now, blank=True)
    profile_image = models.ImageField(default='default.png', upload_to='profile_pics')
    
    def __str__(self):
    	return self.username

"""
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    joined_date = models.DateField(default=datetime.date.today)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.user.username + ' Profile'
"""

class School(models.Model):
    name = models.CharField(max_length=300)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)

    def __str__(self):
    	return self.name
