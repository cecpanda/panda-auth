from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group, Permission


class Department(models.Model):
    name        = models.CharField('部门', unique=True, max_length=10)
    code        = models.CharField('代码', unique=True, max_length=5)
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('permissions'),
        blank=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = "部门"
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        self.code = self.code.lower()
        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.name}'


class Room(models.Model):
    name       = models.CharField('科室', unique=True, max_length=10)
    code       = models.CharField('代码', unique=True, max_length=10)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='rooms', verbose_name='部门')
    groups     = models.ManyToManyField(Group, related_name='rooms', blank=True, verbose_name='团队/组')
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('permissions'),
        blank=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = "科室"
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        self.code = self.code.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.department.name}-{self.name}'


class User(AbstractUser):
    '''
    Department > Room >< Group > User
                  V      GroupExtra
                 User
    '''
    # username
    realname = models.CharField('真名',  max_length=10,  blank=True, null=True, help_text='长度不大于10')
    email    = models.EmailField('邮箱', max_length=30,  blank=True, null=True)
    mobile   = models.CharField("手机",  max_length=20,  blank=True, null=True)
    avatar   = models.ImageField('头像', blank=True, null=True, upload_to='avatars/%Y/%m', default="avatars/default.jpeg")
    gender   = models.CharField("性别",  max_length=1, choices=(("M", "男"), ("F", "女")), default="M")
    job      = models.CharField('职位',  max_length=10,  blank=True, null=True)
    brief    = models.TextField('简介',  blank=True, null=True)

    # 用户只能加入一个科室，权限只看 Group，和 Department/Room/Team 无关
    room     = models.ForeignKey(Room, on_delete=models.PROTECT, blank=True, null=True, related_name='users', verbose_name='科室')

    class Meta:
        ordering = ('id',)
        verbose_name        = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f'{self.username}'


class GroupInfo(models.Model):
    group = models.OneToOneField(Group, on_delete=models.PROTECT, related_name='info', verbose_name='团队/组')
    code  = models.CharField('代码', unique=True, max_length=15)
    desc  = models.TextField(verbose_name='描述', blank=True, null=True)

    class Meta:
        verbose_name = '团队'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        self.code = self.code.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.group}'
