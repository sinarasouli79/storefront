from djoser.serializers import \
    UserCreateSerializer as DjoserUserCreateSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        fields = ['id', 'email', 'username',
                  'password', 'first_name', 'last_name']


class UserSerializer(DjoserUserSerializer):
    username = serializers.CharField(help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                                     validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta(DjoserUserSerializer.Meta):
        fields = ['email', 'id', 'username', 'first_name', 'last_name']
        ref_name = 'CoreSerializer'  # add for drf-yasg library
