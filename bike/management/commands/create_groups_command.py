from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from bike.models import User

class Command(BaseCommand):
    help = 'Create user groups programmatically'

    def handle(self, *args, **options):
        # Create the 'worker' group
        worker_group, created = Group.objects.get_or_create(name='worker')
        # Create the 'mechanic' group
        mechanic_group, created = Group.objects.get_or_create(name='mechanic')

        # add user to group
        user = User.objects.get(username='username')
        worker_group.user_set.add(user)
        