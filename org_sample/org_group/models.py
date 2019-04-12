from django.db import models
from django.contrib.auth.models import Group

from organizations.models import Organization
from organizations.managers import ActiveOrgManager, OrgManager


class GroupOrganization(Organization):

    group = models.OneToOneField(
        Group, on_delete=models.CASCADE, null=False, primary_key=True, verbose_name='Organization group'
    )
    objects = OrgManager()
    active = ActiveOrgManager()
