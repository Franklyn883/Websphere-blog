from django.contrib import admin
from django.contrib.auth import get_user_model 
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUsercreationForm
from .models import Profile


@admin.register(Profile)
class Profile(admin.ModelAdmin):
    pass
    

CustomUser = get_user_model()
#Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUsercreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        "username",
        "first_name",
        "last_name",
        
    ]
    
admin.site.register(CustomUser,CustomUserAdmin)

