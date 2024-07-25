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
    edit_reply,
    delete_reply,
    add_comment,
    edit_comment,
    search_view
)

urlpatterns = [
    path("create/", post_create_view, name="create_blogpost"),
    path("", home_view, name="home"),
    path("post/<uuid:pk>/", post_detail_view, name="blogpost_detail"),
    path("post/comment/<pk>/", add_comment, name="comment-add"),
    path("post/comment/edit/<pk>/", edit_comment, name="comment-edit"),
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
    path("comment/delete/<pk>/", delete_comment, name="comment-delete"),
    path("comment/reply/<pk>/", add_reply, name="comment-reply"),
    path("post/<pk>/like/", like_post_view, name="like-post"),
    path("post/<pk>/bookmark/", bookmark_post_view, name="bookmark-post"),
    path("post/comment/reply/edit/<pk>/", edit_reply, name="reply-edit"),
    path("post/comment/reply/delete/<pk>/", delete_reply, name="reply-delete"),
    path("search-result/",search_view, name="search"),
   
]
