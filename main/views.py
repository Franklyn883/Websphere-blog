from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from blogpost.models import Post
# Create your views here.

class HomePageView(ListView):
    model = Post
    template_name = "main/index.html"  