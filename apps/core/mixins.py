class CompanyQuerysetMixin:

    def get_company_queryset(self, model):

        user = self.request.user

        if user.is_superadmin:
            return model.objects.all()

        return model.objects.filter(company=user.company)