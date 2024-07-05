from django.contrib import admin
from .models import Post,Category,PostComment,LikedPost

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title',  'author','created_at')

admin.site.register(PostComment)
admin.site.register(Post, PostAdmin)
admin.site.register(LikedPost)
admin.site.register(Category)

