from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate, sender=None)
def add_main_permissions(sender, **kwargs):
    from .permissions import add_main_permissions_to_manager_group
    add_main_permissions_to_manager_group()