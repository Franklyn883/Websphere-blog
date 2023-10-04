from django.urls import path
from .views import UserProfileUpdateView

urlpatterns = [

    path('update/<int:pk>', UserProfileUpdateView.as_view(), name='profile_update'),
]
