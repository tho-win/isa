from django.urls import path

from . import views

urlpatterns = [
	path('posts/', views.show_all_posts, name='show_all_posts'),
    path('posts_by_seller/<int:seller_id>/', views.get_posts_by_seller, name='get_posts_by_seller'),
    path('users/', views.show_all_users, name='show_all_users'),
    path('authenticators/', views.show_all_authenticators, name='show_all_authenticators'),
    path('users/<int:uid>/', views.user_detail, name='user_detail'),
    path('posts/<int:pid>/', views.post_detail, name='post_detail'),
    path('create_user/', views.create_user, name='create_user'),
    path('login/', views.login, name='login'),
    path('check_auth/', views.check_auth, name='check_auth'),
    path('create_listing/', views.create_listing, name='create_listing'),
    path('delete/auth/<str:auth>', views.delete_auth, name='delete_auth'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('search_listing/', views.search_listing, name='search_listing'),
    path('listing_views/', views.listing_views, name='listing_views'),
]