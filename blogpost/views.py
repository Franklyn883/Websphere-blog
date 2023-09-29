from django.shortcuts import render
from .forms import PostForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Post
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from blogpost.models import Post
# Create your views here.

class HomePageView(ListView):
    model = Post
    template_name = "blogpost/index.html"  

class BlogPostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'blogpost/blogpost_create.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.cover_img = self.request.FILES.get('cover_img') 
        response = super().form_valid(form)
        self.object.categories.set(form.cleaned_data['categories'])
        return response


class BlogPostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blogpost/blogpost_detail.html'
    context_object_name = 'post'
