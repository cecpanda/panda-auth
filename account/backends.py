"""
主要为了权限问题，重写认证后端
"""

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


UserModel = get_user_model()


class MyBackend(ModelBackend):
    """
    ModelBackend 中的的方法：
        _get_user_permissions
        _get_group_permissions
        _get_permissions
        get_user_permissions
        get_group_permissions
        get_all_permissions

    自定义的方法：
    """

    def _get_user_permissions(self, user_obj):
        return user_obj.user_permissions.all()

    def _get_group_permissions(self, user_obj):
        user_groups_field = get_user_model()._meta.get_field('groups')
        user_groups_query = 'group__%s' % user_groups_field.related_query_name()
        return Permission.objects.filter(**{user_groups_query: user_obj})

    def _get_room_permissions(self, user_obj):
        '''
        返回成员所在科室的权限，注意用户科室是多对一
        '''
        return Permission.objects.filter(room__users=user_obj)

    def _get_department_permissions(self, user_obj):
        return Permission.objects.filter(department__rooms__users=user_obj)


    def _get_permissions(self, user_obj, obj, from_name):
        """
        Return the permissions of `user_obj` from `from_name`. `from_name` can
        be either "group" or "user" to return permissions from
        `_get_group_permissions` or `_get_user_permissions` respectively.
        """
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()

        perm_cache_name = '_%s_perm_cache' % from_name
        if not hasattr(user_obj, perm_cache_name):
            if user_obj.is_superuser:
                perms = Permission.objects.all()
            else:
                perms = getattr(self, '_get_%s_permissions' % from_name)(user_obj)
            perms = perms.values_list('content_type__app_label', 'codename').order_by()
            setattr(user_obj, perm_cache_name, {"%s.%s" % (ct, name) for ct, name in perms})
        return getattr(user_obj, perm_cache_name)

    def get_user_permissions(self, user_obj, obj=None):
        """
        Return a set of permission strings the user `user_obj` has from their
        `user_permissions`.
        """
        return self._get_permissions(user_obj, obj, 'user')

    def get_group_permissions(self, user_obj, obj=None):
        """
        Return a set of permission strings the user `user_obj` has from the
        groups they belong.
        """
        return self._get_permissions(user_obj, obj, 'group')

    def get_room_permissions(self, user_obj, obj=None):
        return self._get_permissions(user_obj, obj, 'room')

    def get_department_permissions(self, user_obj, obj=None):
        return self._get_permissions(user_obj, obj, 'department')

    def get_all_permissions(self, user_obj, obj=None):
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()
        if not hasattr(user_obj, '_perm_cache'):
            user_obj._perm_cache = {
                *self.get_user_permissions(user_obj),
                *self.get_group_permissions(user_obj),
                *self.get_room_permissions(user_obj),
                *self.get_department_permissions(user_obj),
            }
        return user_obj._perm_cache