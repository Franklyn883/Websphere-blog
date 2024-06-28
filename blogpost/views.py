from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .forms import PostForm, PostCommentForm
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Post, Category, PostComment
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import Profile



# Create your views here.


def home_view(request):
    """Display the home view."""
    posts = Post.objects.all()
    categories = Category.objects.all()
    context = {"posts":posts,"categories":categories}
    return render(request, 'blogpost/index.html',context)


@login_required
def post_create_view(request):
    form = PostForm()
    context = {"form":form}
    
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid:
            post = form.save(commit=False)
            post.author = request.user
            post.cover_img = request.FILES.get('cover_img')
            post.save()
            form.save_m2m()
            messages.success(request, "Post created successfully")
            return redirect('home')
            
    return render(request,'blogpost/blogpost_create.html', context)

# class BlogPostDetailView(LoginRequiredMixin, DetailView):
#     """Renders the full details of a blogpost"""

#     model = Post
#     template_name = "blogpost/blogpost_detail.html"
#     context_object_name = "post"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["comments"] = PostComment.objects.filter(post=self.object)
#         context["form"] = PostCommentForm()
#         return context

#     def post(self, request, *arg, **kwargs):
#         post = self.get_object()
#         form = PostCommentForm(request.POST)

#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.author = self.request.user
#             comment.save()
#             return redirect("blogpost_detail", pk=post.pk)
#         else:
#             context = self.get_context_data()
#             context["form"] = form
#             return self.render_to_response(context)
def post_detail_view(request,pk):
    post = get_object_or_404(Post,id=pk)
    comments = post.post_comments.all().order_by("-created_at")
    form = PostCommentForm()
    if request.method == "POST":
       comment = PostComment.objects.create(author=request.user,post=post, comment=request.POST.get('comment'))
        
    context = {"post":post,"comments":comments,"form":form}
    return render(request,"blogpost/blogpost_detail.html",context)

class EditCommentView(LoginRequiredMixin, UpdateView):
    model = PostComment
    form_class = PostCommentForm
    template_name = "blogpost/edit_comment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment"] = self.get_object()
        return context

    def get_success_url(self):
        return reverse_lazy(
            "blogpost_detail", kwargs={"pk": self.object.post.pk}
        )

    def form_valid(self, form):
        form.instance.edited = True
        return super().form_valid(form)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(PostComment, id=comment_id, author=request.user)
    post_id = comment.post.id
    comment.delete()
    return redirect("blogpost_detail", pk=post_id)


class PostCategoryFilterView(ListView):
    """Renders all post related to a selected category."""

    model = Post
    template_name = "blogpost/category_filtered_posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        """Get a category and all it related posts"""
        category = get_object_or_404(Category, id=self.kwargs["pk"])
        return Post.objects.filter(categories=category)

    def get_context_data(self, **kwargs):
        """Get the related fields, categories, so it can be rendered in the template"""
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class BlogpostUpdateView(LoginRequiredMixin, UpdateView):
    """Update blogpost."""

    form_class = PostForm
    queryset = Post.objects.all()
    template_name = "blogpost/blogpost_create.html"


class BlogpostDeleteView(LoginRequiredMixin, DeleteView):
    """Delete blogpost"""

    model = Post
    success_url = reverse_lazy("home")


class SearchResultsListView(ListView):
    """Implement search functionality"""

    model = Post
    context_object_name = "post_list"
    template_name = "blogpost/search_results.html"

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        if query:
            return Post.objects.filter(
                Q(title__icontains=query)
                | Q(subtitle__icontains=query)
                | Q(author__username__icontains=query)
                | Q(categories__name__icontains=query)
            )

        else:
            return Post.objects.all()


class AuthorBlogpostList(LoginRequiredMixin, ListView):
    """Render all blogpost related to a user."""

    model = Post
    template_name = "blogpost/authorblogpost.html"
    context_object_name = "posts"

    def get_queryset(self):
        user = get_object_or_404(
            get_user_model(), username=self.kwargs.get("username")
        )
        return Post.objects.filter(author=user)
