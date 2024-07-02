from django.shortcuts import render
from .forms import PostForm, PostCommentForm
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Post, Category, PostComment
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.


def home_view(request):
    """Display the home view. and filter displayed post."""
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    posts = Post.objects.filter(
        Q(title__icontains=q)
        | Q(subtitle__icontains=q)
        | Q(author__username__icontains=q)
        | Q(categories__name__icontains=q)
    )
    categories = Category.objects.all()
    context = {"posts": posts, "categories": categories}
    return render(request, "blogpost/index.html", context)


@login_required
def post_create_view(request):
    """Creates a new post."""
    form = PostForm()
    context = {"form": form}

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if "cover_img" in request.FILES:
                post.cover_img = request.FILES.get("cover_img")
            post.save()
            form.save_m2m()
            messages.success(request, "Post created successfully")
            return redirect("home")

    return render(request, "blogpost/blogpost_create.html", context)


def post_detail_view(request, pk, comment_id=None):
    """Render, the post with the given pk in details.Gets the post with the pk, 
    then if the comment_id is present in the url, the comment with the id is 
    updated, else a new instance is created."""
    post = get_object_or_404(Post, id=pk)

    # we check if the comment_id is present in the url,if it's present we get the comment with the id and get the right post the id belongs to.This will be use to edit the correct comment.
    if comment_id:
        comment = get_object_or_404(
            PostComment, id=comment_id, post=post, author=request.user
        )

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

    context = {
        "post": post,
        "comments": comments,
        "form": form,
        "comment_id": comment_id,
    }
    return render(request, "blogpost/blogpost_detail.html", context)


@login_required
def delete_comment(request, comment_id):
    """Deletes comment with the given id, where the author is the request user."""
    comment = get_object_or_404(PostComment, id=comment_id, author=request.user)
    post_id = comment.post.id
    if request.method == "POST":
        comment.delete()
        messages.success(request, "Comment deleted successfully")
        return redirect("blogpost_detail", pk=post_id)
    context = {"obj": "your comment"}
    return render(request, "blogpost/confirm_delete.html", context)


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


@login_required
def post_update_view(request, pk):
    """Updates post with the given id, when the author is the request user."""
    post = get_object_or_404(Post, id=pk, author=request.user)
    form = PostForm(instance=post)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if "cover_img" in request.FILES:
                post.cover_img = request.FILES.get("cover_img")
            post.save()
            form.save_m2m()
            messages.success(request, "Post updated successfully")
            return redirect("blogpost_detail", pk=post.id)
        else:
            messages.error(
                request,
                "There was an error updating the post. Please try again.",
            )
    context = {"form": form}
    return render(request, "blogpost/blogpost_create.html", context)


@login_required(login_url="/login")
def post_delete_view(request, pk):
    """Deletes the post where id=pk and the author is the request user."""
    post = get_object_or_404(Post, id=pk, author=request.user)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect("home")
    return render(request, "blogpost/confirm_delete.html", {"obj": post})


# class SearchResultsListView(ListView):
#     """Implement search functionality"""

#     model = Post
#     context_object_name = "post_list"
#     template_name = "blogpost/search_results.html"

#     def get_queryset(self):  # new
#         query = self.request.GET.get("q")
#         if query:
#             return Post.objects.filter(
#                 Q(title__icontains=query)
#                 | Q(subtitle__icontains=query)
#                 | Q(author__username__icontains=query)
#                 | Q(categories__name__icontains=query)
#             )

#         else:
#             return Post.objects.all()


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
