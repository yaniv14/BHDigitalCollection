from django.contrib import admin
from django.utils.translation import ugettext as _
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


class OriginAreaAdmin(admin.ModelAdmin):
    list_display = ('title', 'countries_list')
    list_display_links = ('title', 'countries_list')

    def countries_list(self, obj):
        return ",".join([x.name for x in obj.countries])

    countries_list.short_description = _('Countries')


admin.site.register(models.Artifact, ArtifactAdmin)
admin.site.register(models.ArtifactType)
admin.site.register(models.ArtifactMaterial)
admin.site.register(models.PageBanner, PageBannerAdmin)
admin.site.register(models.OriginArea, OriginAreaAdmin)
