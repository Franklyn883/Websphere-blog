from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.BlogPostCreateView.as_view(), name="create_blogpost"),
    path('get_tag_suggestions/', views.get_tag_suggestions, name='get_tag_suggestions'),

]