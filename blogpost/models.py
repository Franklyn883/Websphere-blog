from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
import uuid
from ckeditor.fields import RichTextField

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class Post(models.Model):
    User = get_user_model()
    id = models.UUIDField(
    primary_key=True,
    default=uuid.uuid4,editable=False)
   
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=100)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    cover_img = models.ImageField(upload_to='post_covers/', blank=True)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.id)])
    
    
