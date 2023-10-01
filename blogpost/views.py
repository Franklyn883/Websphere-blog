from django.shortcuts import render
from .forms import PostForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Post,Category
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
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

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


class PostCategoryFilterView(ListView):
    model = Post
    template_name = 'blogpost/category_filtered_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        category = get_object_or_404(Category, id=self.kwargs['pk'])
        return Post.objects.filter(categories=category)
  
