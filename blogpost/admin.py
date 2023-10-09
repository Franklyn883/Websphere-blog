from django.contrib import admin
from .models import Post,Category


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'author', 'tag_list')

    #using prefetch_related() to minimize queries as recommed in official docs
    #https://django-taggit.readthedocs.io/en/latest/admin.html#including-tags-in-modeladmin-list-display
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

admin.site.register(Post, PostAdmin)
