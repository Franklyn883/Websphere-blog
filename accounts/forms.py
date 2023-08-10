from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

class CustomUsercreationForm(UserCreationForm):
    class meta:
        model = get_user_model()
        fields =("email","username")
        
class CustomUserChangeForm(UserChangeForm):
    class meta:
        model = get_user_model()
        fields = ("email", "username")