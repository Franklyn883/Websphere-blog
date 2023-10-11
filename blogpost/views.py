from django.shortcuts import render
from .forms import PostForm
from django.views.generic import ListView, DetailView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Post,Category
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

    # @login_required(login_url='account_login')
    # def create_post(request):
#     if request.method == 'POST':
#         post_form = PostForm(data=request.POST, files=request.FILES)
#         if post_form.is_valid():
#             new_post = post_form.save(commit=False)
#             new_post.author = request.user
#             profile = Profile.objects.get(profile_user=request.user)
#             new_post.slug = slugify(new_post.title)
            
#             new_post.save()
#             post_form.save_m2m()
#             messages.success(request, 'Post created successfully', extra_tags='post_saved')
#             # redirect to new created item detail view
#             return redirect(new_post.get_absolute_url())
#     else:
#         post_form = PostForm()
#     context = {'post_form': post_form}
#     return render(request,
#                   'blogpost/blogpost_create.html',
#                   context)

class BlogPostDetailView(LoginRequiredMixin, DetailView):
    '''Renders the full details of a blogpost'''
    model = Post
    template_name = 'blogpost/blogpost_detail.html'
    context_object_name = 'post'


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
    
def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    # Filter posts by tag name  
    posts = Post.objects.filter(tags=tag)
    context = {
        'tag':tag,
        'posts':posts,
    }
    return render(request, 'blog/index.html', context)
    
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