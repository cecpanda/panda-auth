from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
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
    department = serializers.SerializerMethodField()
    room = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'username', 'realname', 'email', 'mobile', 'avatar',
                  'gender', 'job', 'brief', 'department', 'room', 'groups')
        model = UserModel

    def get_department(self, obj):
        try:
            name = obj.room.department.name
        except Exception:
            name = None
        return name

    def get_room(self, obj):
        try:
            name = obj.room.name
        except Exception:
            name = None
        return name

    def get_groups(self, obj):
        return [ group.name for group in obj.groups.all()]



class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'username', 'realname', 'avatar')
        model = UserModel


# class PermSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         fields = ('name', 'codename')
#         model = Permission


class PermissionSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()
    room = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    class Meta:
        fields = ('username', 'realname', 'department', 'room', 'permissions')
        model = UserModel

    def get_department(self, obj):
        try:
            name = obj.room.department.name
        except Exception:
            name = None
        return name

    def get_room(self, obj):
        try:
            name = obj.room.name
        except Exception:
            name = None
        return name

    def get_permissions(self, obj):
        permissions = self.init_permissions()

        for app_label, models in permissions.items():
            for model in models.keys():
                if obj.has_perm(f'{app_label}.view_{model}'):
                    permissions[app_label][model]['view'] = True

                if obj.has_perm(f'{app_label}.add_{model}'):
                    permissions[app_label][model]['add'] = True

                if obj.has_perm(f'{app_label}.change_{model}'):
                    permissions[app_label][model]['change'] = True
                    permissions[app_label][model]['view'] = True

                if obj.has_perm(f'{app_label}.delete_{model}'):
                    permissions[app_label][model]['delete'] = True
        return permissions

    def init_permissions(self):
        permissions = dict()
        app_labels = set()

        for ct in ContentType.objects.all():
            app_labels.add(ct.app_label)

        try:
            app_labels.remove('sessions')
            app_labels.remove('contenttypes')
            app_labels.remove('auth')
            app_labels.remove('admin')
        except KeyError:
            pass

        for app_label in app_labels:
            permissions[app_label] = dict()
            for ct in ContentType.objects.filter(app_label=app_label):
                permissions[app_label][ct.model] = {"view": False, "add": False, "change": False, "delete": False}

        return permissions
