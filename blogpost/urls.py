from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.BlogPostCreateView.as_view(), name="create_blogpost"),

]