from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import (Department, Room)
from .serializers import (DepartmentSerializer,
                          RoomSerializer,
                          UserSerializer,
                          PermissionSerializer)
from .utils import UserPagination


UserModel = get_user_model()


class DepartmentViewSet(ListModelMixin,
                        RetrieveModelMixin,
                        GenericViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class RoomViewSet(ListModelMixin,
                  RetrieveModelMixin,
                  GenericViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class UserViewSet(ListModelMixin,
                  RetrieveModelMixin,
                  GenericViewSet):
    lookup_field = 'username'
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPagination
    # permission_classes = [IsAuthenticated,]

    def get_permissions(self):
        if self.action == 'get_info':
            return []
        return [IsAuthenticated()]

    @action(methods=['get'], detail=False, url_path='info', url_name='info')
    def get_info(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PermissionView(GenericAPIView):
    serializer_class = PermissionSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)
