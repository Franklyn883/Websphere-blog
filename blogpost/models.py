from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
import uuid
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    

    
class Post(models.Model):
    User = get_user_model()
    id = models.UUIDField(
    primary_key=True,
    default=uuid.uuid4,editable=False)
   
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    cover_img = models.ImageField(upload_to='post_covers/', blank=True, null=True)
    categories = models.ManyToManyField(Category)
    tags = TaggableManager()
    
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("blogpost_detail", args=[str(self.id)])
    
    
