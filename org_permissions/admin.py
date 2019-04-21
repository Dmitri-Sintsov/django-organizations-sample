from django.contrib import admin

from .models import OrganizationPermission


admin.site.register(OrganizationPermission, admin.ModelAdmin)
