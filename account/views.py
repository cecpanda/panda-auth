from django.contrib.auth import get_user_model
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated

from .models import (Department, Room)
from .serializers import (DepartmentSerializer,
                          RoomSerializer,
                          UserSerializer)
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
    permission_classes = [IsAuthenticated,]
