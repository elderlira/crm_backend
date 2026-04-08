from apps.users.models import User

def get_available_agents(department_id):

    agents = User.objects.filter(
        userdepartment__department_id=department_id,
        no_auto_assign=False,
        is_active=True
    )

    return agents