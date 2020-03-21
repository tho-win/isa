from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import *
from .models import *
from rest_framework.decorators import action

class CustomUserViewSet(viewsets.ModelViewSet):
	serializer_class = CustomUserSerializer

	def get_queryset(self):
		queryset = CustomUser.objects.all()
		username = self.request.query_params.get('username', None)
		if username is not None:
			queryset = queryset.filter(username=username)
		return queryset

class AuthenticatorViewSet(viewsets.ModelViewSet):
	serializer_class = AuthenticatorSerializer
	
	def get_queryset(self):
		queryset = Authenticator.objects.all()
		auth = self.request.query_params.get('authenticator', None)
		if auth is not None:
			queryset = queryset.filter(authenticator=auth)
		return queryset


class PostViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all().order_by('-pub_date')
	serializer_class = PostSerializer


class SchoolViewSet(viewsets.ModelViewSet):
	queryset = School.objects.all().order_by('name')
	serializer_class = SchoolSerializer