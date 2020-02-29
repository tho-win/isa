from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    password = models.CharField(max_length=100, default="password")
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    computing_id = models.CharField(max_length=10, default="")
    phone_number = models.CharField(max_length=20, blank=True)
    bio = models.TextField(max_length=100, blank=True)
    date_joined = models.DateTimeField(default=timezone.now, blank=True)
    profile_image = models.ImageField(default='default.png', upload_to='profile_pics')
    
    def __str__(self):
    	return self.username


# class Profile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     image = models.ImageField(default='default.png', upload_to='profile_pics')
#     joined_date = models.DateField(default=datetime.date.today)

#     def __repr__(self):
#         return str(self)

#     def __str__(self):
#         return self.user.username + ' Profile'


class Post(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="")
    content = models.TextField(max_length=3000, default="")
    pub_date = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # remaining swipes the seller wants to sell
    remaining_nums = models.IntegerField()
    # the location where seller will meet the buyer and swipe him/her in
    pickup_address = models.CharField(max_length=300, default="")

    def __repr__(self):
        return str(self)

    def __str__(self):
        retStr = self.title + " created by " + str(self.seller)
        return retStr

    def was_published_in_30days(self):
        now = timezone.now()
        return now - datetime.timedelta(days=30) <= self.pub_date <= now

    def was_published_in_90days(self):
        now = timezone.now()
        return now - datetime.timedelta(days=90) <= self.pub_date <= now



class School(models.Model):
    name = models.CharField(max_length=300)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)

    def __str__(self):
    	return self.name
