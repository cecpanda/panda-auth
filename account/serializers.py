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


class ChangeAvatarSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('avatar',)
        model = UserModel


class ChangeProfileSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('realname', 'email', 'mobile', 'gender', 'job', 'brief')
        model = UserModel


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(style={'input_type': 'password'})
    new_password = serializers.CharField(style={'input_type': 'password'})


class UserInfoSerializer(serializers.ModelSerializer):
    menu = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'username', 'realname', 'avatar', 'menu')
        model = UserModel

    def get_menu(self, obj):
        '''
        前端根据这个列表动态渲染导航
        menu = [
            'it',
            'member',
            'it-sys',
            'it-sys-tft',
            'it-sys-lcd',
            'it-eq',
            'tft',
            'tft-cvd',
            'tft-pho'
        ]
        '''
        menu = []
        # 部门和科室的导航直接通过判断确定
        # 剩下的导航根据权限
        if obj.has_perm('menu.is_manager'):
            menu.append('manager')
        elif obj.has_perm('menu.is_leader'):
            menu.append('leader')
        else:
            menu.append('member')

        try:
            menu.append(obj.room.department.code)
            menu.append(obj.room.code)
        except Exception:
            pass

        # 三级导航通过权限的 view 判定
        # 找到所有服务，看是否有 view 权限
        for service in ContentType.objects.all():
            p = f'{service.app_label}.view_{service.name}'
            if obj.has_perm(p):
                menu.append(service.name)
        return menu


class PermissionSerializer(serializers.Serializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    action = serializers.ChoiceField(label='动作', choices=(('view', 'add', 'change', 'delete')))
    app = serializers.CharField(label='应用', required=True)
    service = serializers.CharField(label='服务', required=True)

    def validate(self, attrs):
        app = attrs.get('app')
        service = attrs.get('service')
        if not ContentType.objects.filter(app_label=app, model=service).exists():
            raise serializers.ValidationError(f'不存在您指定的app: {app}，或不存在service: {service}.')
        return attrs


class PermissionsSerializer(serializers.ModelSerializer):
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
