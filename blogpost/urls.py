from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.BlogPostCreateView.as_view(), name="create_blogpost"),
    path('', views.HomePageView.as_view(), name="home" ),
    path('<uuid:pk>/', views.BlogPostDetailView.as_view(), name='blogpost_detail'),
    path('category/<uuid:pk>/', views.PostCategoryFilterView.as_view(), name='category_filter'),
]