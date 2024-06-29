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
    context = {"posts": posts, "categories": categories}
    return render(request, "blogpost/index.html", context)


@login_required
def post_create_view(request):
    form = PostForm()
    context = {"form": form}

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid:
            post = form.save(commit=False)
            post.author = request.user
            post.cover_img = request.FILES.get("cover_img")
            post.save()
            form.save_m2m()
            messages.success(request, "Post created successfully")
            return redirect("home")

    return render(request, "blogpost/blogpost_create.html", context)


# def post_detail_view(request, pk):
#     post = get_object_or_404(Post, id=pk)
#     comments = post.post_comments.all().order_by("-created_at")
#     form = PostCommentForm()
#     if request.method == "POST":
#         form = PostCommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.author = request.user
#             comment.post = post
#             comment.save()
#             return redirect("blogpost_detail", pk=post.id)

#     context = {"post": post, "comments": comments, "form": form}
#     return render(request, "blogpost/blogpost_detail.html", context)


def post_detail_view(request, pk, comment_id=None):
    post = get_object_or_404(Post, id=pk)
    
    if comment_id:
        comment = get_object_or_404(PostComment, id=comment_id, post=post)
       
    else:
        comment = None
      
    if request.method == "POST":
        if comment:
            form = PostCommentForm(request.POST, instance=comment)
        else:
            form = PostCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            if comment:
                new_comment.edited = True
            new_comment.save()
            return redirect("blogpost_detail", post.id)
    else:
        if comment:
            form = PostCommentForm(instance=comment)
        else:
            form = PostCommentForm()
            
    comments = post.post_comments.all().order_by("-created_at")

    context = {"post": post, "comments": comments, "form": form,  'comment_id': comment_id,}
    return render(request, "blogpost/blogpost_detail.html", context)


def edit_comment_view(request, pk):
    comment = get_object_or_404(PostComment, id=pk)
    form = PostCommentForm(instance=comment)
    context = {"form": form}
    if request.method == "POST":
        form = PostCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save(commit=False)
            form.edited = True
            form.save()
            messages.success(request, "Comment updated")
            return redirect("blogpost_detail", comment.post.pk)

    return render(request, "blogpost/edit_comment.html", context)


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
