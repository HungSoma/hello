from django.db import models
from  django.db.models.signals import post_save
from  django.contrib.auth.models import User
# Create your models here.

#
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, related_name = "user")
#     birthday = models.DateField(null=True, blank=True)
#     bio = models.TextField(default='', blank=True)
#     country = models.CharField(max_length = 100,default='', blank = True)
#     city = models.CharField(max_length = 50 ,default='', blank = True)
#     organization = models.CharField(max_length = 100,default='', blank = True)
# def create_profile(sender, **kwargs):
#     user = kwargs["instance"]
#     if kwargs["create"]:
#         user_profile = UserProfile(user = user)
#         user_profile.save()
# post_save.connect(create_profile, sender =User)