from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import *
from .models import *


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = CustomUserSerializer


# class ProfileViewSet(viewsets.ModelViewSet):
# 	queryset = Profile.objects.all().order_by('user')
# 	serializer_class = ProfileSerializer


class PostViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all().order_by('-pub_date')
	serializer_class = PostSerializer


class SchoolViewSet(viewsets.ModelViewSet):
	queryset = School.objects.all().order_by('name')
	serializer_class = SchoolSerializer