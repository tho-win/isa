from django.urls import include, path
from rest_framework import routers
from api import views
from .views import *

router = routers.DefaultRouter()
router.register(r'user', CustomUserViewSet, basename="customuser")
router.register(r'post', PostViewSet, basename="post")
router.register(r'school', SchoolViewSet, basename="school")
router.register(r'authenticator', AuthenticatorViewSet, basename="authenticator")
router.register(r'recommendation', RecommendationViewSet, basename="recommendation")


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('get_user/<int:uid>/', views.get_user, name='get_user'),
    path('delete_recomm/', views.delete_recomm, name='delete_recomm'),
    path('create_recomm/', views.create_recomm, name='create_recomm'),
    path('get_recomm/<int:pid>/', views.get_recomm, name='get_recomm'),
]