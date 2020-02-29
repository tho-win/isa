from django.urls import include, path
from rest_framework import routers
from api import views
from .views import *


router = routers.DefaultRouter()
router.register(r'user', CustomUserViewSet)
router.register(r'post', PostViewSet)
router.register(r'school', SchoolViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]