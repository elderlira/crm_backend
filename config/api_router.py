from rest_framework.routers import DefaultRouter

from apps.clients.views import ClientViewSet
from apps.closing_reasons.views import ClosingReasonViewSet
from apps.departments.views import DepartmentViewSet 
from apps.permissions.views import PermissionViewSet
from apps.profiles.views import ProfileViewSet
from apps.users.views import UserViewSet
from apps.companies.views import CompanyViewSet
from apps.labels.views import LabelViewSet

router = DefaultRouter()

router.register(r"clients", ClientViewSet, basename="clients")

router.register(r"closing-reasons",ClosingReasonViewSet,basename="closing-reasons")

router.register(r"departments", DepartmentViewSet, basename="departments")

router.register(r"permissions", PermissionViewSet, basename="permissions")

router.register(r"profiles", ProfileViewSet, basename="profiles")

router.register(r"users", UserViewSet, basename="users")

router.register(r"companies", CompanyViewSet, basename="companies")

router.register(r"labels",LabelViewSet, basename="labels")

urlpatterns = router.urls