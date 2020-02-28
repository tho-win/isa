from . import views
from django.urls import path, include

app_name = 'frontend'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('users/', views.show_all_users, name='show_all_users'),
    path('users/<int:uid>/', views.user_detail, name='user_detail'),
]