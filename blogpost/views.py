from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .forms import PostForm, PostCommentForm
from django.views.generic import ListView, DetailView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Post,Category,PostComment
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import Profile

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from blogpost.models import Post
# Create your views here.

class HomePageView(ListView):
    '''Render all the blogpost in the database'''
    model = Post
    template_name = "blogpost/index.html"  
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        '''Get the related fields, categories, so it can be rendered in the template'''
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    def get(self, request, *args, **kwargs):
        tag = self.request.GET.get("tag")
        if tag:
            posts = Post.objects.filter(tags__name__in=[tag]) # tags filtered by tag parameter
        else:
            posts = Post.objects.all()
        return render(request, 'blogpost/index.html', {'posts': posts, 'categories': Category.objects.all()})


class BlogPostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    '''Creates Blog post'''
    form_class = PostForm
    model = Post
    template_name = 'blogpost/blogpost_create.html'
    success_message = " Post Added Successfully"
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        '''validates form and ensure proper saving of the many to many fields'''
        form.instance.author = self.request.user
        form.instance.cover_img = self.request.FILES.get('cover_img') 
        response = super().form_valid(form)
        print(self.object)  # Add this line
        self.object.categories.set(form.cleaned_data['categories'])
        return response


class BlogPostDetailView(LoginRequiredMixin, DetailView):
    '''Renders the full details of a blogpost'''
    model = Post
    template_name = 'blogpost/blogpost_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = PostComment.objects.filter(post=self.object)
        context['form'] = PostCommentForm()
        return context
    
    def post(self, request, *arg, **kwargs):
        post = self.get_object()
        form = PostCommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = self.request.user
            comment.save()
            return redirect('blogpost_detail', pk=post.pk)
        else:
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)
        

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(PostComment,id=comment_id,author = request.user)
    
    if request.method == 'POST':
        form = PostCommentForm(request.POST,instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blogpost_detail',pk=comment.post.id)
        
    else:
        form = PostCommentForm(instance=comment)
        
    return render(request, 'edit_comment.html',{'form':form})
    
    
    
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(PostComment, id=comment_id, author=request.user)
    post_id = comment.post.id
    comment.delete()
    return redirect('blogpost_detail',pk=post_id)

class PostCategoryFilterView(ListView):
    '''Renders all post related to a selected category'''
    model = Post
    template_name = 'blogpost/category_filtered_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        ''' Get a category and all it related posts '''
        category = get_object_or_404(Category, id=self.kwargs['pk'])
        return Post.objects.filter(categories=category)
    def get_context_data(self, **kwargs):
        '''Get the related fields, categories, so it can be rendered in the template'''
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    

  

class BlogpostUpdateView(LoginRequiredMixin, UpdateView):
    ''' Update blogpost'''
    form_class = PostForm
    queryset = Post.objects.all()
    template_name = 'blogpost/blogpost_create.html'
    
class BlogpostDeleteView(LoginRequiredMixin, DeleteView):
    '''Delete blogpost'''
    model = Post
    success_url = reverse_lazy('home')
    
    
class SearchResultsListView(ListView):
    '''Implement search functionality'''
    model = Post
    context_object_name = 'post_list'
    template_name = 'blogpost/search_results.html'
    
    def get_queryset(self): # new
        query = self.request.GET.get("q")
        if query:
            return Post.objects.filter(
            Q(title__icontains=query) | Q(subtitle__icontains=query)
           |Q(author__username__icontains=query) | Q(categories__name__icontains=query) ) 
            
        else:
            return Post.objects.all()
    
class AuthorBlogpostList(LoginRequiredMixin, ListView):
    '''Render all blogpost related to a user'''
    model = Post
    template_name ='blogpost/authorblogpost.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        user = get_object_or_404(get_user_model(),username=self.kwargs.get('username'))
        return Post.objects.filter(author = user)