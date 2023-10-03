from django.contrib import admin
from .models import Post,Category

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','created_at','author')
admin.site.register(Category)

admin.site.register(Post,PostAdmin)