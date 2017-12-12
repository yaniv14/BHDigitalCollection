from django.contrib import admin
from . import models


class ArtifactImageInline(admin.TabularInline):
    model = models.ArtifactImage
    extra = 1


class ArtifactAdmin(admin.ModelAdmin):
    inlines = [
        ArtifactImageInline,
    ]


admin.site.register(models.Artifact, ArtifactAdmin)
