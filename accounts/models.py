from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model
from django.urls import reverse
from PIL import Image
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

    
class Profile(models.Model):
    User = get_user_model()
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile',null=True)
    profile_pic = models.ImageField(upload_to='profile_images/', default='default.jpg')
    phone_number = PhoneNumberField(blank=True, null=True)
    country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.TextField(null=True,blank=True)
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=gender_choices, null=True, blank=True)
    tech_stack = models.CharField(max_length=255,blank=True,null=True)
    github = models.URLField(blank=True, null=True)
    linkedIn = models.URLField(blank=True,null=True)
    facebook = models.URLField(blank=True, null=True) 
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    # Override the save method of the model
    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.profile_pic.path) # Open image
        # resize image
        if img.height > 100 or img.width > 100:
            output_size = (100, 100)
            img.thumbnail(output_size) # Resize image
            img.save(self.profile_pic.path)  # Save it again and override the larger image
    
    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'pk': self.pk})
