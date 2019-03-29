from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group


class Department(models.Model):
    name = models.CharField('部门', max_length=10)

    class Meta:
        ordering = ('id',)
        verbose_name = "部门"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name}'


class Room(models.Model):
    name = models.CharField('科室', max_length=10)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='rooms', verbose_name='部门')

    class Meta:
        ordering = ('id',)
        verbose_name = "科室"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.department.name}/{self.name}'


# 修改了原来的 Group，makemigrations 时带来不想要的结果
# Group.add_to_class('room', models.ForeignKey(Room, on_delete=models.PROTECT, related_name='groups', verbose_name='科室'))


# class Team(Group):
#     # 不能添加字段，弃用
#
#     class Meta:
#         proxy = True


# Department > Room > Team = Group > User

class Team(models.Model):
    group = models.OneToOneField(Group, on_delete=models.PROTECT, related_name='team',  verbose_name='团队')
    room  = models.ForeignKey(Room,     on_delete=models.PROTECT, related_name='teams', verbose_name='科室')
    desc = models.TextField(max_length=30, verbose_name='团队描述')

    class Meta:
        ordering = ('id',)
        verbose_name = '团队'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.room.department.name}/{self.room.name}/{self.group.name}"


class User(AbstractUser):
    # username
    realname = models.CharField('真名',  max_length=10,  blank=True, null=True, help_text='长度不大于10')
    email    = models.EmailField('邮箱', max_length=30,  blank=True, null=True)
    mobile   = models.CharField("手机",  max_length=20,  blank=True, null=True)
    avatar   = models.ImageField('头像', blank=True, null=True, upload_to='avatars/%Y/%m', default="avatars/default.jpeg")
    gender   = models.CharField("性别",  max_length=1, choices=(("M", "男"), ("F", "女")), default="M")

    # 用户只能加入一个科室，权限只看 Group，和 Department/Room/Team 无关
    room     = models.ForeignKey(Room, on_delete=models.PROTECT, blank=True, null=True, related_name='users', verbose_name='科室')

    class Meta:
        ordering = ('id',)
        verbose_name        = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f'{self.username}'

