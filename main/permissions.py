from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import CustomPermissions


def add_main_permissions_to_manager_group():
    manager_group, created = Group.objects.get_or_create(name='manager')

    can_disable_mailing_permission = Permission.objects.get(
        codename='can_disable_mailing',
        content_type=ContentType.objects.get_for_model(CustomPermissions)
    )
    manager_group.permissions.add(can_disable_mailing_permission)
    manager_group.save()
