from django.urls import path

from . import views

urlpatterns = [
	path('posts/', views.show_all_posts, name='show_all_posts'),
    path('users/', views.show_all_users, name='show_all_users'),
    path('users/<int:uid>/', views.user_detail, name='user_detail'),
    path('posts/<int:pid>/', views.post_detail, name='post_detail'),
    path('create_user/', views.create_user, name='create_user'),
    path('login/', views.login, name='login'),
    path('check_auth/', views.check_auth, name='check_auth'),
    path('delete/auth/<str:auth>', views.delete_auth, name='delete_auth'),
]