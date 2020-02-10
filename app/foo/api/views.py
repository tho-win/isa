#from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .serializers import *
from users import models as users_models
from swipeme import models as swipeme_models
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = users_models.CustomUser.objects.all().order_by('username')
    serializer_class = CustomUserSerializer

class ProfileViewSet(viewsets.ModelViewSet):
	queryset = users_models.Profile.objects.all().order_by('user')
	serializer_class = ProfileSerializer

class SchoolViewSet(viewsets.ModelViewSet):
	queryset = swipeme_models.School.objects.all().order_by('name')
	serializer_class = SchoolSerializer