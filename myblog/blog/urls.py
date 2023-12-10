# blog/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import post_detail, add_comment, toggle_share, profile
from .views import register, home, login_view, logout_view, search_view
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

app_name = 'blog'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home, name='home'),
    path('profile/', profile, name='profile'),
    path('search/', search_view, name='search_results'),
    path('post/', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/add_comment/', add_comment, name='add_comment'),
    path('post/<int:pk>/toggle_share/', toggle_share, name='toggle_share'),
]
