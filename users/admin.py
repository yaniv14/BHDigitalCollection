import copy
from authtools.admin import UserAdmin as UA
from django.contrib import admin

from users.models import ArtifactContact
from . import models


class UserAdmin(UA):
    list_display = (
        'email',
        'full_name',
        'phone',
        'is_active',
        'is_staff',
        'is_superuser',
        'last_login',
    )

    fieldsets = copy.deepcopy(UA.fieldsets)
    fieldsets[0][1]['fields'] = fieldsets[0][1]['fields'] + (
        'full_name',
        'phone',
    )

    date_hierarchy = "last_login"

    list_filter = (
        'is_superuser',
        'is_staff',
        'is_active',
    )


class ArtifactContactAdmin(admin.ModelAdmin):
    list_display = ('submitted_at', 'name', 'email', 'phone')
    list_display_links = ('submitted_at', 'name', 'email', 'phone')


admin.site.register(models.User, UserAdmin)
admin.site.register(ArtifactContact, ArtifactContactAdmin)
