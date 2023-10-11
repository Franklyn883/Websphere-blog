from django.urls import path
from .views import ( HomePageView,BlogpostDeleteView,PostCategoryFilterView,BlogPostDetailView,
                    BlogpostUpdateView,SearchResultsListView,BlogPostCreateView)
urlpatterns = [
    # path("r'^create/$'", create_post, name="create_blogpost"),
    path('create/',BlogPostCreateView.as_view(), name='create_blogpost'),
    path('', HomePageView.as_view(), name="home" ),
    path('<uuid:pk>/', BlogPostDetailView.as_view(), name='blogpost_detail'),
    path('category/<uuid:pk>/', PostCategoryFilterView.as_view(), name='category_filter'),
    path('update/<uuid:pk>/', BlogpostUpdateView.as_view(), name="update_blogpost"),
    path('delete/<uuid:pk>/', BlogpostDeleteView.as_view(), name='delete_blogpost'),
    path('search/', SearchResultsListView.as_view(), name="search_results"),
]