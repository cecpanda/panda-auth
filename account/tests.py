from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

from .models import Department, Room


UserModel = get_user_model()


class BackendTestCase(TestCase):

    def setUp(self):
        d = Department.objects.create(name="信息工程部")
        r = Room.objects.create(name='CIM', department=d)
        u = UserModel.objects.create_user(username='durant', password='cecpanda123', room=r)

        p1 = Permission.objects.get(codename='add_department')
        p2 = Permission.objects.get(codename='change_department')
        p3 = Permission.objects.get(codename='add_room')
        p4 = Permission.objects.get(codename='change_room')

        d.permissions.add(p1)
        r.permissions.add(p2)

        u.user_permissions.add(p4)

    def test_get_room_permissions(self):
        user = UserModel.objects.get(username='durant')
        p = Permission.objects.filter(room__users=user)


    def test_get_department_permissions(self):
        user = UserModel.objects.get(username='durant')
        p = Permission.objects.filter(department__rooms__users=user)

    def test_get_all_permissions(self):
        user = UserModel.objects.get(username='durant')
        p = user.get_all_permissions()
        print(p)
