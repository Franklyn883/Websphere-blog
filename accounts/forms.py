from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms

class CustomUsercreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = get_user_model()
        fields = ('username','first_name', 'last_name', 'email', 'password1', 'password2')
        
        
        
class CustomUserChangeForm(UserChangeForm):
    class meta:
        model = get_user_model()
        fields = ("email", "username")