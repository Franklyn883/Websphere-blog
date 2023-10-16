from django.urls import path,include, re_path
from .views import UserProfileView, profile_update

urlpatterns = [
    path('update/', profile_update, name="profile_update"),
    path('<int:pk>/', UserProfileView.as_view(), name='user_profile'),
  
]
