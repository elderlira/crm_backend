from rest_framework.viewsets import ModelViewSet


class BaseCompanyViewSet(ModelViewSet):

    def get_queryset(self):

        user = self.request.user

        queryset = super().get_queryset()

        if user.is_superadmin:
            return queryset

        return queryset.filter(company=user.company)