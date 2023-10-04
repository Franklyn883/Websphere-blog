from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model
from django.urls import reverse
import uuid
# Create your models here.

#creating current user

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254, unique=True)
   
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'pk': self.user_profile.user.pk})


class Technology(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    User = get_user_model()
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True, default=None)
    profile_pic = models.ImageField(upload_to='profile_pic/', blank=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.TextField(null=True,blank=True)
    sex_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    sex = models.CharField(max_length=1, choices=sex_choices, null=True, blank=True)
    tech_stack = models.ManyToManyField(Technology, blank=True)
    social_media_links = models.OneToOneField('SocialMedia', on_delete=models.CASCADE,null=True, blank=True, default=None)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'pk': self.pk})
    
class SocialMedia(models.Model):
    twitter = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    linkedIn = models.URLField(blank=True,null=True)
    facebook = models.URLField(blank=True, null=True)   
    
    def __str__(self):
        return f"social media links for {self.user_profile.user.username}"