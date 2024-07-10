from django.urls import path
from .views import  profile_update, profile_view,follow_user,unfollow_user

urlpatterns = [
    path('update/', profile_update, name="profile_update"),
    path("<str:username>",profile_view, name="userprofile"),
    path("",profile_view,name="profile"),
    path("<username>/follow/",follow_user, name="follow-user"), 
    path("<username>/unfollow", unfollow_user,name="unfollow-user"),
  
]
