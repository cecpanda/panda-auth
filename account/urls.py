from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (DepartmentViewSet, RoomViewSet, UserViewSet, PermissionView)


app_name = 'account'

router = DefaultRouter()
router.register('department', DepartmentViewSet, base_name='department')
router.register('room',       RoomViewSet,       base_name='room')
router.register('user',       UserViewSet,       base_name='user')


urlpatterns = [
    path('', include(router.urls)),
    path('permission/', PermissionView.as_view())
]
