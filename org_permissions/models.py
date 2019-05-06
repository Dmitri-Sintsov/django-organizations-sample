from django.db import models
from django.contrib.auth.models import Permission
from django.core import management

from organizations.models import Organization


class OrganizationPermissionManager(models.Manager):

    def add_user(self, organization_name, user, create_initial=False):
        if create_initial:
            management.call_command('create_organizations_permissions')
        org, created = Organization.objects.get_or_create(name=organization_name)
        # We will assign organization admin / owner manually in Django Admin.
        org.add_user(user, is_admin=False)
        return org, created

    def remove_user(self, organization_name, user, create_initial=False):
        if create_initial:
            management.call_command('create_organizations_permissions')
        org, created = Organization.objects.get_or_create(name=organization_name)
        org.users.remove(user)
        return org, created


class OrganizationPermission(models.Model):
    organization = models.OneToOneField(
        Organization, on_delete=models.CASCADE, related_name='org_perm', null=False, primary_key=True, verbose_name='Organization'
    )
    # Many Permission to many OrganizationPermission.
    permissions = models.ManyToManyField(
        Permission, verbose_name='Permissions'
    )

    objects = OrganizationPermissionManager()

    class Meta:
        verbose_name = 'Organization permission'
        verbose_name_plural = 'Organization permissions'

    def __str__(self):
        return '{} : {}'.format(str(self.organization), ' : '.join(str(perm) for perm in self.permissions.all()))
