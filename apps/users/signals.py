from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserDepartment, UserCompanyDepartment

@receiver(post_save, sender=UserDepartment)
def populate_user_company_department(sender, instance, created, **kwargs):
    if created:
        user_company = instance.user.company

        if user_company:
            UserCompanyDepartment.objects.get_or_create(
                user=instance.user,
                company=user_company,
                department=instance.department
            )

            from apps.departments.models import CompanyDepartment

            CompanyDepartment.objects.get_or_create(
                company=user_company,
                department=instance.department,
                defaults={'active': True}
            )