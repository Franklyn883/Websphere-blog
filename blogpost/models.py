from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
import uuid
from django_ckeditor_5.fields import CKEditor5Field
from PIL import Image
from taggit.managers import TaggableManager
from django.utils.text import slugify

# Create your models here.

User = get_user_model()
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, null=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Post(models.Model):
    """A model of a post, with relevant fields."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    content = CKEditor5Field("Text", config_name="extends")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="post"
    )
    cover_img = models.ImageField(
        upload_to="post_covers/", blank=True, null=True
    )
    categories = models.ManyToManyField(Category, related_name="posts")
    likes = models.ManyToManyField(User, related_name="likes", through="LikedPost")

    def save(self, *args, **kwargs):
        super().save()
        if self.cover_img:
            try:
                img = Image.open(self.cover_img.path)
                # Perform operations with the image if needed
                if img.height > 840 or img.width > 1600:
                    output_size = (840, 1600)
                    img.thumbnail(output_size)
                    img.save(self.cover_img.path)
            except FileNotFoundError:
                # Handle the case where the file is not found
                pass
            
    class Meta:
        ordering = ["-created_at","-updated_at"]    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blogpost_detail", args=[str(self.id)])

class BookMark(models.Model):
    """A models for a post bookmark"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="bookmarks")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user','post')
        
class PostComment(models.Model):
    """A model of the post comments."""
  
    post = models.ForeignKey(
        Post, related_name="post_comments", on_delete=models.CASCADE
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    comment = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)
    

    def get_absolute_url(self):
        """returns the url of the comment."""
        return reverse("blogpost_detail", args=[str(self.id)])
    
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.comment

class Reply(models.Model):
    """A model of the post comments."""
    User = get_user_model()
    parent_comment = models.ForeignKey(
        PostComment, related_name="replies", on_delete=models.CASCADE
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="replies")
    body = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)

    def get_absolute_url(self):
        """returns the url of the comment."""
        return reverse("blogpost_detail", args=[str(self.id)])

    def __str__(self):
        return self.body
    
class LikedPost(models.Model):
    """A through table for the likes field in the post models."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username}: {self.post.title}"