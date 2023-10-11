from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from .models import Profile


class CustomUsercreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = get_user_model()
        fields = ('username','first_name', 'last_name', 'email', 'password1', 'password2')
        
        
#update user information
class CustomUserChangeForm(UserChangeForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    class Meta:
       model = get_user_model()
       fields = ('username', 'first_name', 'last_name', 'email')
       
#update user profile
class UserProfileUpdateForm(forms.ModelForm):
    tech_stack = forms.CharField(widget=forms.Textarea, required=False) 
    photo=forms.ImageField(widget=forms.FileInput)
    bio = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Profile
        fields = ['user', 'photo', 'phone_number', 'location', 'bio', 'gender', 'tech_stack', 'twitter', 'github', 'linkedIn', 'facebook']
  
    

    