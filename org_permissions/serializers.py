from rest_framework import serializers

from organizations.models import OrganizationUser

from .models import OrganizationPermission


class OrganizationUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = OrganizationUser
        fields = ['id', 'organization', 'user']
        datatables_always_serialize = ['id']


class OrganizationPermissionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = OrganizationPermission
        fields = ['id', 'organization', 'permissions']
        datatables_always_serialize = ['id']
