from rest_framework import serializers
from users import models as users_models
from swipeme import models as swipeme_models

class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = users_models.CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'bio')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = users_models.Profile
		fields = ('user', 'joined_date')


class SchoolSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = swipeme_models.School
		fields = ('name', 'city', 'state')
