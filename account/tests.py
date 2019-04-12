import json
from pprint import pprint

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase, RequestFactory, Client
from rest_framework.test import APITestCase, APIRequestFactory, APIClient, RequestsClient

from .views import UserViewSet
from .models import Department, Room
from .utils import fake


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


class UserViewSetTestCase(TestCase):

    def setUp(self):
        self.client = Client()  # 默认已经定义好了，client_class = Client self.client = self.client_class()
        self.factory = RequestFactory()

        d = Department.objects.create(name="信息工程部")
        r = Room.objects.create(name='CIM', department=d)
        user_list = []
        for _ in range(50):
            user_list.append(UserModel(username=fake.user_name(), password='123', room=r))
        UserModel.objects.bulk_create(user_list)

    def test_user_viewset_by_client(self):
        user = UserModel.objects.all()[0]
        self.client.force_login(user=user)
        r = self.client.get('/account/user/')
        r = r.json()
        self.assertEqual(r.get('count'), 50)

    def test_user_viewset_by_factory(self):
        request = self.factory.get('/account/user/')
        user = UserModel.objects.all()[0]
        request.user = user
        response = UserViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.data.get('count'), 50)


class UserViewSetAPITestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()  # client_class = APIClient
        self.request = RequestsClient()
        self.factory = APIRequestFactory()

        d = Department.objects.create(name="信息工程部")
        r = Room.objects.create(name='CIM', department=d)
        user_list = []
        for _ in range(50):
            user_list.append(UserModel(username=fake.user_name(), password='123', room=r))
        UserModel.objects.bulk_create(user_list)

    def test_user_viewset_by_client(self):
        user = UserModel.objects.all()[0]
        self.client.force_authenticate(user=user)
        r = self.client.get('/account/user/')
        self.assertEqual(r.data.get('count'), 50)

    def test_user_viewset_by_factory(self):
        request = self.factory.get('/account/user/')
        user = UserModel.objects.all()[0]
        request.user = user
        response = UserViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.data.get('count'), 50)


class UserInfoTestCase(APITestCase):

    def setUp(self):
        self.request = RequestsClient()

        d = Department.objects.create(name="信息工程部")
        r = Room.objects.create(name='CIM', department=d)
        UserModel.objects.create(username="durant", password="123", room=r)

    def test_get_info(self):
        user = UserModel.objects.get(username='durant')

        self.client.credentials(HTTP_AUTHORIZATION='JWT 123')
        res = self.client.get('/account/info/')
        pprint(res)
        pprint(res.data)
