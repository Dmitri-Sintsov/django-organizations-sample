from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.utils.module_loading import import_string
from django.contrib.auth.models import Permission

from organizations.models import Organization

from ...models import OrganizationPermission


class Command(BaseCommand):
    # Django command help
    help = 'Setup initial organizations and permissions.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--app-names',
            action='store_true',
            dest='app_names',
            default='org_permissions',
            help='Comma-separated apps list used to get initial organizations and permissions from.'
        )

    def setup_organizations(self, permissions=None):
        for organization_name, perm_list in permissions.items():
            organization, created = Organization.objects.get_or_create(name=organization_name)
            action = 'Created' if created else 'Loaded'
            self.stdout.write('{} organization "{}"'.format(action, organization_name))
            for perm in perm_list:
                app_label, codename = perm.split('.')
                permission = Permission.objects.filter(content_type__app_label=app_label, codename=codename).first()
                if permission is None:
                    raise CommandError('No such permission: %s' % perm)
                organization_permission, created = OrganizationPermission.objects.get_or_create(organization=organization)
                action = 'Created' if created else 'Loaded'
                organization_permission.permissions.add(permission)
                self.stdout.write('{} organization permission "{}"'.format(action, perm))

    def setup_app(self, app_name):
        permissions = import_string('{}.permissions'.format(app_name))
        self.setup_organizations(permissions=permissions.DEFAULT_ORGANIZATION_PERMISSIONS)

    def handle(self, *args, **options):
        for app_name in options['app_names'].split(','):
            self.setup_app(app_name)
