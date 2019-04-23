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
                          ChangeProfileSerializer,
                          ChangePasswordSerializer,
                          UserInfoSerializer,
                          PermissionSerializer,
                          PermissionsSerializer)
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
        elif self.action == 'change_profile':
            return ChangeProfileSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        elif self.action == 'get_permission':
            return PermissionSerializer
        return UserSerializer

    @action(methods=['post'], detail=False, url_path='change-avatar', url_name='change_avatar')
    def change_avatar(self, request):
        user = request.user
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'avatar': serializer.data.get('avatar')}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='change-profile', url_name='change_profile')
    def change_profile(self, request):
        user = request.user
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='change-password', url_name='change_password')
    def change_password(self, request):
        user = request.user
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        if user.check_password(serializer.validated_data.get('old_password')):
            user.set_password(serializer.validated_data.get('new_password'))
            user.save()
            return Response({'status': 'ok'}, status.HTTP_202_ACCEPTED)
        return Response({'error': 'wrong password'}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='get-permission', url_name='get_permission')
    def get_permission(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        action_name = serializer.data.get('action')
        app = serializer.data.get('app')
        service = serializer.data.get('service')
        if user.has_perm(f'{app}.{action_name}_{service}'):
            return Response({'allowed': True}, status=status.HTTP_200_OK)
        else:
            return Response({'allowed': False}, status=status.HTTP_200_OK)


class UserInfoView(GenericAPIView):
    serializer_class = UserInfoSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class PermissionsView(GenericAPIView):
    serializer_class = PermissionsSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)
