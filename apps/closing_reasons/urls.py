from rest_framework.routers import DefaultRouter
from .views import ClosingReasonViewSet


router = DefaultRouter()

router.register(
    "",
    ClosingReasonViewSet,
    basename="closing-reasons"
)

urlpatterns = router.urls