from django.shortcuts import render
from .forms import PostForm, PostCommentForm, ReplyForm
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Post, Category, PostComment, BookMark, Reply
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.views import is_following


# Create your views here.


def home_view(request):
    """Display the home view and filter displayed post."""
    q = request.GET.get("q") if request.GET.get("q") != None else ""
   
    posts = Post.objects.filter(
        Q(title__icontains=q)
        | Q(subtitle__icontains=q)
        | Q(author__username__icontains=q)
        | Q(categories__name__icontains=q)
    ).distinct()
    bookmarked_posts = []
    categories = Category.objects.all()
  
    posts_with_follow_status = []
    if request.user.is_authenticated:
            for post in posts:
                posts_with_follow_status.append((post, is_following(request.user, post.author)))
            bookmarked_posts = request.user.bookmarks.values_list('post__id', flat=True)
    else:
            for post in posts:
                posts_with_follow_status.append((post, False))  # Default to False for non-authenticated users



       
    
    for post in posts:
        post.is_bookmarked = post.id in bookmarked_posts
   
    
    context = {
        "posts": posts,
        "categories": categories,
        "posts_with_follow_status":posts_with_follow_status
        
    }
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


def post_detail_view(request, pk):
    """Display all the post details, where the pk = post id."""
    post = get_object_or_404(Post, id=pk)
    reply_form = ReplyForm()
    comment_form = PostCommentForm()
    comments = post.post_comments.all()
    is_following_author = is_following(request.user, post.author)
    post.is_bookmarked = request.user.is_authenticated and post.id in request.user.bookmarks.values_list('post__id', flat=True)

    context = {
        "post": post,
        "comment_form": comment_form,
        "reply_form": reply_form,
        "is_following_author": is_following_author,
        "comments": comments
    }
    return render(request, "blogpost/blogpost_detail.html", context)


@login_required
def add_comment(request, pk):
    """Add a comment to a post"""
    post = get_object_or_404(Post, id=pk)
    comment_form = PostCommentForm()
    if request.method == "POST":
        comment_form = PostCommentForm(request.POST)
        if comment_form.is_valid:
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, "Comment added!")

    context = {"comment": comment, "post": post}
    return render(request, "blogpost/snippets/_add_comment.html", context)


@login_required
def edit_comment(request, pk):
    """Edit comment with the given pk."""
    comment = get_object_or_404(PostComment, id=pk, author=request.user)
    comment_form = PostCommentForm(instance=comment)
    post = comment.post
    if request.method == "POST":
        comment_form = PostCommentForm(request.POST, instance=comment)
        if comment_form.is_valid:
            comment = comment_form.save(commit=False)
            comment.edited = True
            messages.success(request, "Comment updated successfully!")
            comment.save()
            return redirect("blogpost_detail", comment.post.id)
    context = {"comment_form": comment_form}
    return render(request, "blogpost/partials/_edit_comment.html", context)


@login_required
def delete_comment(request, pk):
    """Deletes comment with the given id, where the author is the request user."""
    comment = get_object_or_404(PostComment, id=pk, author=request.user)
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
        """Get the related fields, categories, so it can be rendered in the
        template"""
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


@login_required
def add_reply(request, pk):
    """Add reply to a comment with the specified id."""
    comment = get_object_or_404(PostComment, id=pk)
    post_id = comment.post.id
    if request.method == "POST":
        print(request.POST)
        form = ReplyForm(request.POST)
        if form.is_valid:
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment
            reply.save()
            messages.success(request, "New reply added")
    return redirect("blogpost_detail", post_id)


@login_required
def edit_reply(request, pk):
    reply = get_object_or_404(Reply, id=pk, author=request.user)
    reply_form = ReplyForm(instance=reply)
    if request.method == "POST":
        reply_form = ReplyForm(request.POST, instance=reply)
        if reply_form.is_valid:
            reply_form.save()
            messages.success(request, "reply updated!")

            return redirect("blogpost_detail", reply.parent_comment.post.id)

    context = {"reply_form": reply_form}

    return render(request, "blogpost/edit_reply.html", context)


def delete_reply(request, pk):
    reply = get_object_or_404(Reply, id=pk, author=request.user)
    if request.method == "POST":
        reply.delete()
        messages.success(request, "Reply deleted successfully")
        return redirect("blogpost_detail", reply.parent_comment.post.id)
    context = {"obj": reply}
    return render(request, "blogpost/confirm_delete.html")


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


def like_post_view(request, pk):
    """Add like to a post, if the request user is not the author of the post.
    Then checks if the user already exits in the likes table, if the user exits
    remove user, else add the user.To implement the like and unlike feature"""
    post = get_object_or_404(Post, id=pk)
    user_exit = post.likes.filter(username=request.user.username).exists()
    if request.user != post.author:
        if user_exit:
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

    return render(request, "blogpost/snippets/_likes.html", {"post": post})


def bookmark_post_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    bookmark, created = BookMark.objects.get_or_create(
        user=request.user, post=post
    )
    if not created:
        bookmark.delete()
        messages.success(request, "Removed from Bookmark")
    else:
        messages.success(request, "Added to Bookmark")

    post.is_bookmarked = request.user.is_authenticated and post.id in request.user.bookmarks.values_list('post__id', flat=True)
    context = {"post": post}

    return render(request, "blogpost/snippets/_add_bookmark.html", context)
