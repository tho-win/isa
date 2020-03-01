from . import views
from django.urls import path, include

app_name = 'frontend'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('posts/', views.show_all_posts, name="show_all_posts"),
  	path('specialposts', views.show_special_posts, name="show_special_posts"),
    path('users/', views.show_all_users, name='show_all_users'),
    path('users/<int:uid>/', views.user_detail, name='user_detail'),
]