from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.

#creating current user

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30,blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=254, unique=True)
   
    def __str__(self):
        return self.username