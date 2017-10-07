from django.db import models
from  django.db.models.signals import post_save
from  django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="user")
    Gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    first_name = models.CharField(null = True, blank = True, default = '', max_length = 20)
    last_name = models.CharField(null=True, blank=True, default='', max_length=20)
    gender = models.CharField(blank = True, default = '', max_length = 2, choices = Gender_choices)
    birthday = models.DateField(null=True, blank=True)
    bio = models.TextField(default='', blank=True, max_length = 1000)
    #phone = models.CharField(null = True, blank = True, default = '', max_length = 12)
    country = models.CharField(max_length = 100,default='', blank = True)
    city = models.CharField(max_length = 50 ,default='', blank = True)
    organization = models.CharField(max_length = 100,default='', blank = True)
def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile.objects.create(user = user)
        user_profile.save()
post_save.connect(create_profile, sender =User)