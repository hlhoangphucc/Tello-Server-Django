from rest_framework import serializers
from django.contrib.auth.models import User

from api.models import InfoUser, Message, Posts, User


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = "__all__"


class InfoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoUser
        fields = "__all__"
