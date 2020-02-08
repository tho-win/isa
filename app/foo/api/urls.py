from django.urls import include, path
from rest_framework import routers
from .views import *
from api import views

router = routers.DefaultRouter()
router.register(r'user', CustomUserViewSet)
router.register(r'profile', ProfileViewSet)
router.register(r'school', SchoolViewSet)

urlpatterns = [
    path('', include(router.urls)),
    #path('user/<int:pk>/', views.user_detail_by_id),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]