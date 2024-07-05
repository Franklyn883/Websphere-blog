from django.urls import path
from .views import (
    home_view,
    post_delete_view,
    PostCategoryFilterView,
    post_detail_view,
    post_update_view,
    post_create_view,
    AuthorBlogpostList,
    delete_comment,
    add_reply,
    like_post_view,
    bookmark_post_view,
    
)

urlpatterns = [
    path("create/", post_create_view, name="create_blogpost"),
    path("", home_view, name="home"),
    path("post/<uuid:pk>/", post_detail_view, name="blogpost_detail"),
    path(
        "post/<uuid:pk>/comment/<int:comment_id>",
        post_detail_view,
        name="blogpost_detail_comment",
    ),
    path(
        "category/<uuid:pk>/",
        PostCategoryFilterView.as_view(),
        name="category_filter",
    ),
    path("update/<uuid:pk>/", post_update_view, name="update_blogpost"),
    path("post/delete/<uuid:pk>/", post_delete_view, name="delete_blogpost"),
    path(
        "userposts/<str:username>",
        AuthorBlogpostList.as_view(),
        name="user-posts",
    ),
    path(
        "comment/delete/<int:comment_id>/",
        delete_comment,
        name="delete-comment",
    ),
    path("comment/reply/<comment_id>/", add_reply, name="comment-reply"),
    path("post/<pk>/like/", like_post_view, name="like-post"),
    path("post/<pk>/bookmark/", bookmark_post_view, name="bookmark-post")
]
