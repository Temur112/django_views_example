from django.contrib.auth.models import User, Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.get(id=3)
        group, created = Group.objects.get_or_create(
            name="profile manager",
        )
        permission_profile = Permission.objects.get(codename="view_userprofile")
        permission_log_entry = Permission.objects.get(codename="view_logentry")

        group.permissions.add(permission_profile)
        user.groups.add(group)

        user.user_permissions.add(permission_log_entry)
        group.save()
        user.save()
        self.stdout.write("Operations completed")



