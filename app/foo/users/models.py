import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    bio = models.TextField(max_length=100, blank=True)
    
    def __str__(self):
    	return self.username


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    joined_date = models.DateField(default=datetime.date.today)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.user.username + ' Profile'