from django.shortcuts import render
from .forms import PostForm, PostCommentForm, ReplyForm
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Post, Category, PostComment, BookMark, Reply, LikedComment, LikedReply
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.views import is_following
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.http import HttpResponse
from django.urls import reverse

# Create your views here.

User = get_user_model()


def home_view(request):
    """Display the home view."""
    posts = (
        Post.objects.all()
        .select_related("author", "author__profile")
        .prefetch_related(
            "categories",
            Prefetch(
                "author", queryset=User.objects.all().select_related("profile")
            ),
            Prefetch("likes", queryset=User.objects.all()),
            Prefetch(
                "post_comments",
                queryset=PostComment.objects.select_related("author"),
            ),
            Prefetch(
                "bookmarks", queryset=BookMark.objects.select_related("post")
            ),
        )
    )
    recent_posts = posts[:5]
    categories = Category.objects.all()
    comments = PostComment.objects.all()
    comments = comments[:5]

    if request.user.is_authenticated:
        bookmarked_posts = set(
            request.user.bookmarks.values_list("post__id", flat=True)
        )
    else:
        bookmarked_posts = set()

    for post in posts:
        post.is_bookmarked = post.id in bookmarked_posts

    categories = Category.objects.all()

    context = {
        "posts": posts,
        "categories": categories,
        "recent_posts": recent_posts,
        "comments": comments,
    }
    return render(request, "blogpost/index.html", context)


def search_view(request):
    """Handle search queries and return search results."""
    query = request.GET.get("q", "")

    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query)
            | Q(subtitle__icontains=query)
            | Q(author__username__icontains=query)
            | Q(categories__name__icontains=query)
        ).distinct()
    else:
        posts = Post.objects.none()

    context = {"posts": posts, "query": query}
    return render(request, "blogpost/search_results.html", context)


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
    post = get_object_or_404(
        Post.objects.select_related(
            "author", "author__profile"
        ).prefetch_related(
            "categories",
            Prefetch("likes", queryset=User.objects.all()),
            Prefetch(
                "post_comments",
                queryset=PostComment.objects.select_related(
                    "author", "author__profile"
                ).prefetch_related(
                    Prefetch(
                        "replies",
                        queryset=Reply.objects.select_related(
                            "author", "author__profile"
                        ).prefetch_related(
                            Prefetch(
                                "likes",
                                queryset=LikedReply.objects.select_related("user"))),
                    ),
                    Prefetch(
                        "likes",
                        queryset=LikedComment.objects.select_related("user"),
                    ),
                ),
            ),
        ),
        id=pk,
    )
    reply_form = ReplyForm()
    comment_form = PostCommentForm()
    comments = post.post_comments.all()
    # Get a list of comment IDs that the user has liked
    liked_comments = set(
        post.post_comments.filter(likes__user=request.user).values_list(
            "id", flat=True
        )
    )
    liked_replies = set(
       Reply.objects.filter(likes__user=request.user, parent_comment__in=post.post_comments.all()).values_list("id", flat=True)
    )
    is_following_author = ""
    if request.user.is_authenticated:
        is_following_author = is_following(request.user, post.author)

    post.is_bookmarked = (
        request.user.is_authenticated
        and post.id in request.user.bookmarks.values_list("post__id", flat=True)
    )

    context = {
        "post": post,
        "comment_form": comment_form,
        "reply_form": reply_form,
        "is_following_author": is_following_author,
        "comments": comments,
        "liked_comments": liked_comments,   
        "liked_replies": liked_replies,
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


@login_required
def delete_reply(request, pk):
    reply = get_object_or_404(Reply, id=pk, author=request.user)
    if request.method == "POST":
        reply.delete()
        messages.success(request, "Reply deleted successfully")
        return redirect("blogpost_detail", reply.parent_comment.post.id)
    context = {"obj": reply}
    return render(request, "blogpost/confirm_delete.html", context)


class AuthorBlogpostList(LoginRequiredMixin, ListView):
    """Render all blogpost related to a user."""

    model = Post
    template_name = "blogpost/authorblogpost.html"
    context_object_name = "posts"

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user)


login_required


def like_post_view(request, pk):
    """Add like to a post, if the request user is not the author of the post.
    Then checks if the user already exits in the likes table, if the user exits
    remove user, else add the user.To implement the like and unlike feature"""
    if not request.user.is_authenticated:
        login_url = request.build_absolute_uri(reverse("account_login"))
        if "HX-Request" in request.headers:
            response = HttpResponse(status=401)
            response["HX-Redirect"] = login_url
            return response

    post = get_object_or_404(Post, id=pk)
    user_exit = post.likes.filter(username=request.user.username).exists()
    if request.user != post.author:
        if user_exit:
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

    return render(request, "blogpost/snippets/_likes.html", {"post": post})


@login_required
def like_comment_view(request, pk):
    """Add like to a comment, if the request user is not the author of the comment."""
    comment = get_object_or_404(PostComment, id=pk)
  
    if request.user != comment.author:
        like = LikedComment.objects.filter(user=request.user, comment=comment).first()
        if like:
            like.delete()
        else:
            LikedComment.objects.create(user=request.user, comment=comment)
    return redirect("blogpost_detail", pk=comment.post.id)

def like_reply_view(request,pk):
    """Add like to a reply, if the request user is not the author of the reply."""
    reply = get_object_or_404(Reply,id=pk)
    if request.user != reply.author:
        like = LikedReply.objects.filter(user=request.user, reply=reply).first()
        if like:
            like.delete()
        else:
            LikedReply.objects.create(user=request.user, reply=reply)
    return redirect("blogpost_detail", pk=reply.parent_comment.post.id)

def bookmark_post_view(request, pk):
    """Bookmark post"""
    if not request.user.is_authenticated:
        login_url = request.build_absolute_uri(reverse("account_login"))
        if "HX-Request" in request.headers:
            response = HttpResponse(status=401)
            response["HX-Redirect"] = login_url
            return response

    post = get_object_or_404(Post, id=pk)
    bookmark, created = BookMark.objects.get_or_create(
        user=request.user, post=post
    )
    if not created:
        bookmark.delete()
        messages.success(request, "Removed from Bookmark")
    else:
        messages.success(request, "Added to Bookmark")

    post.is_bookmarked = (
        request.user.is_authenticated
        and post.id in request.user.bookmarks.values_list("post__id", flat=True)
    )
    context = {"post": post}

    return render(request, "blogpost/snippets/_add_bookmark.html", context)
