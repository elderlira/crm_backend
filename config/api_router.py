from rest_framework.routers import DefaultRouter

from apps.clients.views import ClientsViewSet
from apps.closing_reasons.views import ClosingReasonViewSet
from apps.departments.views import DepartmentsViewSet
from apps.permissions.views import (PermissionViewSet, ProfileViewSet, ProfilePermissionViewSet)

router = DefaultRouter()

router.register(r"clients", ClientsViewSet, basename="clients")

router.register(r"closing-reasons",ClosingReasonViewSet,basename="closing-reasons")

router.register(r"departments", DepartmentsViewSet, basename="departments")

router.register(r"permissions", PermissionViewSet, basename="permissions")

router.register(r"profiles", ProfileViewSet, basename="profiles")

router.register(r"profile-permissions", ProfilePermissionViewSet, basename="profile-permissions")


urlpatterns = router.urls