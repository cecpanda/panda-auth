from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

from .models import Department, Room, GroupExtra


User = get_user_model()


class RoomInline(admin.StackedInline):
    model = Room
    extra = 2
    show_change_link = True
    fieldsets = (
        (None,      {'fields': ('id', 'name')}),
        ('科室权限', {'classes': ('collapse',), 'fields': ('permissions',)}),
    )
    filter_horizontal = ('permissions', )


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'list_rooms')
    search_fields = ('name', 'rooms__name')
    fieldsets = (
        (None,      {'fields': ('id', 'name')}),
        ('权限信息', {'classes': ('collapse',), 'fields': ('permissions',)})
    )
    inlines = (RoomInline,)
    readonly_fields = ('id',)
    filter_horizontal = ('permissions',)

    def list_rooms(self, obj):
        names = []
        for room in obj.rooms.all():
            names.append(room.name)
        return names

    list_rooms.short_description = "科室"


admin.site.register(Department, DepartmentAdmin)


class GroupInline(admin.TabularInline):
    model = GroupExtra
    extra = 2
    show_change_link = True


class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    search_fields = ('name', 'department__name')
    fieldsets = (
        (None,      {'fields': ('id', 'department', 'name')}),
        ('科室权限', {'classes': ('collapse',), 'fields': ('permissions',)}),
        ('团队和组', {'classes': ('collapse',), 'fields': ('groups',)})
    )
    readonly_fields = ('id',)
    filter_horizontal = ('permissions', 'groups')


admin.site.register(Room, RoomAdmin)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('list_group', 'list_rooms')
    fieldsets = (
        (None, {'fields': ('group', 'desc')}),
        # ('团队权限', {'classes': ('collapse',), 'fields': ('group.permissions',)}),
    )

    def list_group(self, obj):
        return obj.group

    list_group.short_description = '团队/组'

    def list_rooms(self, obj):
        names = []
        for room in obj.group.rooms.all():
            names.append(room.name)
        return names

    list_rooms.short_description = "科室"


# admin.site.unregister(Group)
admin.site.register(GroupExtra, GroupAdmin)


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
        ('权限信息', {'classes': ('collapse',), 'fields': ('groups', 'user_permissions')}),
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
            'fields': ('username',
                       'password1',
                       'password2',
                       'realname',
                       'email',
                       'mobile',
                       'gender',
                       'room',
                       'groups',
                       'user_permissions'),
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
