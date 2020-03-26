from django.urls import include, path
from rest_framework import routers
from api import views
from .views import *

router = routers.DefaultRouter()
router.register(r'user', CustomUserViewSet, basename="customuser")
router.register(r'post', PostViewSet, basename="post")
router.register(r'school', SchoolViewSet, basename="school")
router.register(r'authenticator', AuthenticatorViewSet, basename="authenticator")


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('get_user/<int:uid>/', views.get_user, name='get_user')
]