from rest_framework import serializers
from .models import *

class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'url', 'username', 'password', 'email', 'first_name', 'last_name', 'computing_id', 'phone_number', 'bio')


class AuthenticatorSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Authenticator
		fields = ('authenticator', 'user_id', 'date_created')

class PostSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Post
		fields = ('id', 'url', 'seller', 'title', 'content', 'pub_date', 'price', 'remaining_nums', 'pickup_address')


class SchoolSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = School
		fields = ('id', 'url', 'name', 'city', 'state')
