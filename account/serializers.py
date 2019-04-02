from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Department, Room


UserModel = get_user_model()


class RoomForDepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name')
        model = Room


class DepartmentSerializer(serializers.ModelSerializer):
    rooms = RoomForDepartmentSerializer(many=True)

    class Meta:
        fields = ('id', 'name', 'rooms')
        model = Department


class GroupForOthersSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name')
        model = Group


class RoomSerializer(serializers.ModelSerializer):
    groups = GroupForOthersSerializer(many=True)

    class Meta:
        fields = ('id', 'name', 'groups')
        model = Room


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'username', 'realname', 'email', 'mobile', 'avatar',
                  'gender')
        model = UserModel
