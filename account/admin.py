from django.contrib import admin
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

from .models import Department, Room, Team


User = get_user_model()


admin.site.register(Department)
admin.site.register(Room)
admin.site.register(Team)


class MyUserAdmin(UserAdmin):
    list_per_page = 50
    list_display  = ('username', 'id', 'realname', 'email', 'list_department', 'room', 'is_active')
    list_filter   = ('room__department__name', 'room', 'groups', 'is_active')
    search_fields = ('username', 'id', 'realname')

    # 若不设置 fields 和 fieldsets， 默认显示 AutoField 和  editable=True 的字段
    # 如果想显示其他字段，需要加入 readonlu_fields
    fieldsets = (
        ('基本信息', {'fields': ('id', 'username', 'password', 'realname', 'email')}),
        ('详细信息', {'classes': ('collapse',), 'fields': ('avatar', 'mobile', 'gender', 'date_joined', 'is_staff', 'is_superuser', 'is_active')}),
        ('部门信息', {'classes': ('collapse',), 'fields': ('list_department', 'room',)}),
        ('权限信息', {'classes': ('collapse',), 'fields': ('groups', 'user_permissions',)}),
    )
    readonly_fields = ('id', 'list_department')
    filter_horizontal = ('groups', 'user_permissions',)
    ordering = ('id',)

    # 添加用户
    add_form_template = 'admin/auth/user/add_form.html'
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )

    def list_department(self, obj):
        try:
            name = f"{obj.room.department.name}"
        except Exception as e:
            name = None
        return name

    list_department.short_description = '部门'


admin.site.register(User, MyUserAdmin)
