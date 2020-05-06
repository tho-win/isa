from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from .serializers import *
from django.core import serializers as core_serializers
from .models import *
from rest_framework.decorators import action
import json
from django.core.exceptions import ObjectDoesNotExist

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
	serializer_class = PostSerializer

	def get_queryset(self):
		queryset = queryset = Post.objects.all().order_by('-pub_date')
		seller_id = self.request.query_params.get('seller_id', None)
		if seller_id is not None:
			queryset = queryset.filter(seller_id=seller_id)
		return queryset


class SchoolViewSet(viewsets.ModelViewSet):
	queryset = School.objects.all()
	serializer_class = SchoolSerializer


class RecommendationViewSet(viewsets.ModelViewSet):
	queryset = Recommendation.objects.all()
	serializer_class = RecommendationSerializer


def get_user(request, uid):
	if request.method == "POST":
		user = CustomUser.objects.filter(id = uid)[0]
		user.username = request.POST.get('username')
		user.email = request.POST.get('email')
		user.first_name = request.POST.get('first_name')
		user.last_name = request.POST.get('last_name')
		user.computing_id = request.POST.get('computing_id')
		user.phone_number = request.POST.get('phone_number')
		user.bio = request.POST.get('bio')
		user.save()
		return JsonResponse({'ok': True}, safe=False) 
	else:
		return JsonResponse({'ok': False, 'result': 'not post'}, safe=False)


def delete_recomm(request):
	all_recomms = Recommendation.objects.all()
	for recomm in all_recomms:
		recomm.delete()
	return JsonResponse({'ok': True}, safe=False) 


@csrf_exempt
def create_recomm(request):
	if request.method == 'POST':
		item_recomm = json.loads(request.POST.get('data'))
		for key in item_recomm:
			item_id = int(key)
			curr_item = Post.objects.filter(id = item_id)[0]
			curr_recomm = Recommendation.objects.create(
				item = curr_item,
				co_views = json.dumps(item_recomm[key]))
			curr_recomm.save()
		return JsonResponse({'ok': True}, safe=False)
	else:
		return JsonResponse({'ok': False, 'result': 'not post'}, safe=False)


@csrf_exempt
def get_recomm(request, pid):
	item = Post.objects.filter(id = pid)[0]
	try:
		item.recommendation
	except ObjectDoesNotExist:
		return JsonResponse({'ok': False}, safe=False)
	else:	
		return JsonResponse({'ok': True, 'co_views': item.recommendation.co_views}, safe=False)







