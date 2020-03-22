from . import views
from django.urls import path, include
from django.views.generic import TemplateView

app_name = 'frontend'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('posts/', views.show_all_posts, name="show_all_posts"),
  	path('specialposts', views.show_special_posts, name="show_special_posts"),
    path('users/', views.show_all_users, name='show_all_users'),
    path('users/<int:uid>/', views.user_detail, name='user_detail'),
    path('posts/<int:pid>/', views.post_detail, name='post_detail'),
    path('signup', views.sign_up, name="signup"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('logout_success', views.logout_success, name="logout_success")
]