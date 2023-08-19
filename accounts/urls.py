from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.registration, name="signup" ),
    path('login', views.login_page, name="login")
]