from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from accounts.models import BranchDirectory

class Command(BaseCommand):
    help = 'Seed default roles and branches'

    def handle(self, *args, **kwargs):
        for role in ['Admin', 'Manager', 'Worker', 'Auditor']:
            Group.objects.get_or_create(name=role)
        BranchDirectory.objects.get_or_create(name='HQ', defaults={'location': 'Main DC', 'timezone': 'UTC'})
        self.stdout.write(self.style.SUCCESS('Seeded groups and branches'))
