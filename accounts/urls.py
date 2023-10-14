from django.urls import path
from .views import UserProfileView, profile_update,follow_user,unfollow_user

urlpatterns = [
    path('update/', profile_update, name="profile_update"),
    path('<int:pk>/', UserProfileView.as_view(), name='user_profile'),
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow_user')
]
