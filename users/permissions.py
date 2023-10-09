from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import CustomPermissionsForUser


def add_users_permissions_to_manager_group():
    manager_group, created = Group.objects.get_or_create(name='manager')
    can_block_users_permission = Permission.objects.get(
        codename='can_block_users',
        content_type=ContentType.objects.get_for_model(CustomPermissionsForUser)
    )
    manager_group.permissions.add(can_block_users_permission)
    manager_group.save()
