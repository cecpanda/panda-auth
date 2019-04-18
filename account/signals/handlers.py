import random
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import Group
from account.models import GroupInfo


@receiver(post_save, sender=Group, dispatch_uid='add_group_info')
def group_info_handler(sender, **kwargs):
    if kwargs.get('created'):
        group = kwargs.get('instance')
        GroupInfo.objects.create(group=group, code=f'{random.randrange(100000, 999999)}')
