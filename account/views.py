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
                          ChangeAvatarSerializer,
                          UserInfoSerializer,
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
    # serializer_class = UserSerializer
    pagination_class = UserPagination
    permission_classes = [IsAuthenticated,]

    def get_serializer_class(self):
        if self.action == 'change_avatar':
            return ChangeAvatarSerializer
        return UserSerializer

    @action(methods=['post'], detail=False, url_path='change-avatar', url_name='change_avatar')
    def change_avatar(self, request):
        user = request.user
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'avatar': serializer.data.get('avatar')}, status=status.HTTP_200_OK)


class UserInfoViewSet(GenericAPIView):
    serializer_class = UserInfoSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class PermissionView(GenericAPIView):
    serializer_class = PermissionSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)
