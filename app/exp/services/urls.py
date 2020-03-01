from django.urls import path

from . import views

urlpatterns = [
	path('posts/', views.show_all_posts, name='show_all_posts'),
    path('users/', views.show_all_users, name='show_all_users'),
    path('users/<int:uid>/', views.user_detail, name='user_detail'),
]