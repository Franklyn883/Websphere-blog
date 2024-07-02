from django.urls import path
from .views import  profile_update, profile_view

urlpatterns = [
    path('update/', profile_update, name="profile_update"),
    path("<str:username>",profile_view, name="userprofile"),
    path("",profile_view,name="profile")
    
  
]
