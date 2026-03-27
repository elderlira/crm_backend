
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/auth/", include("apps.users.urls")),
    path('clients/', include('apps.clients.urls')),
    path('departments/', include('apps.departments.urls')),
    path('permissions/', include('apps.permissions.urls')),
    path('closing-reasons/', include('apps.closing_reasons.urls')),
]
