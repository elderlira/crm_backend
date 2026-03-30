from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Permite acesso apenas para usuários com Role ID = 1 (Admin)
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.role_id == 1
        )

class IsGerenteUser(permissions.BasePermission):
    """
    Permite acesso para Admin (1) e Gerente (2)
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.role_id in [1, 2]
        )