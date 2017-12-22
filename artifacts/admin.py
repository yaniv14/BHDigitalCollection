from django.contrib import admin
from . import models


class ArtifactImageInline(admin.TabularInline):
    model = models.ArtifactImage
    extra = 1


class ArtifactAdmin(admin.ModelAdmin):
    inlines = [
        ArtifactImageInline,
    ]


class PageBannerAdmin(admin.ModelAdmin):
    list_display = ('page', 'main_text', 'credit', 'active')
    list_display_links = ('page', 'main_text', 'credit', 'active')


admin.site.register(models.Artifact, ArtifactAdmin)
admin.site.register(models.ArtifactType)
admin.site.register(models.ArtifactMaterial)
admin.site.register(models.PageBanner, PageBannerAdmin)
admin.site.register(models.OriginArea)
