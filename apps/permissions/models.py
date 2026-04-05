from django.db import models


class Profile(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Permission(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ProfilePermission(models.Model):

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="profile_permissions"
    )

    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.profile} - {self.permission}"