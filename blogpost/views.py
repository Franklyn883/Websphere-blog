from django.shortcuts import render
from .forms import PostForm
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Post
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'blogpost/blogpost_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        return response
