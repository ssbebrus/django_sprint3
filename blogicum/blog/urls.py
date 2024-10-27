from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('category/<slug:category_slug>/', views.CategoryPosts.as_view(),
         name='category_posts'),
]
