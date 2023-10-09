from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
import uuid
from django_ckeditor_5.fields import CKEditor5Field
from PIL import Image
from taggit.managers import TaggableManager

# Create your models here.

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name
    

    
class Post(models.Model):
    User = get_user_model()
    id = models.UUIDField(
    primary_key=True,
    default=uuid.uuid4,editable=False)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    content = CKEditor5Field('Text', config_name='extends')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    cover_img = models.ImageField(upload_to='post_covers/', blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='posts')
    tags = TaggableManager()
   
    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.cover_img.path) # Open image
        # resize image
        if img.height > 840 or img.width > 1600:
            output_size = (840, 1600)
            img.thumbnail(output_size) # Resize image
            img.save(self.cover_img.path)  # Save it again and override the larger image
    
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("blogpost_detail", args=[str(self.id)])
    
    
