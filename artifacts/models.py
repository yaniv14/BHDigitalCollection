from django.conf import settings
from django.utils.translation import ugettext as _
from django.db import models
from django_countries.fields import CountryField


class ArtifactStatus(object):
    PENDING = 1
    MISSING = 2
    APPROVED = 3
    REJECTED = 4

    choices = (
        (PENDING, _('Pending approval')),
        (MISSING, _('Missing info')),
        (APPROVED, _('Approved')),
        (REJECTED, _('Rejected')),
    )


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=200)
    parent_category = models.ForeignKey('self', verbose_name=_('Parent category'), on_delete=models.SET_NULL, blank=True, null=True, related_name='parents')

    def __str__(self):
        return self.name


class Artifact(models.Model):
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='uploaded_artifacts', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    acceptance_date = models.DateTimeField(blank=True, null=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='approved_artifacts', null=True, blank=True)
    status = models.PositiveSmallIntegerField(_('Status'), choices=ArtifactStatus.choices, default=ArtifactStatus.PENDING)
    is_private = models.BooleanField(_('Privately owned artifact'), default=False)
    name = models.CharField(_('Name'), max_length=250)
    category = models.ForeignKey(Category, verbose_name=_('Category'), on_delete=models.SET_NULL, blank=True, null=True, related_name='artifacts')
    year_era = models.CharField(_('Era/Years range'), max_length=200)
    technical_data = models.TextField(_('Technical data'))
    description = models.TextField(_('Description'))
    short_description = models.TextField(_('Short description'), blank=True, null=True)
    origin_city = models.CharField(_('City'), max_length=100, blank=True, null=True)
    origin_country = CountryField(_('Country'), blank=True, null=True)
    origin_area = models.CharField(_('Area'), max_length=250, blank=True, null=True)
    is_displayed = models.BooleanField(_('Displayed in museum?'), default=False)
    displayed_at = models.CharField(_('Artifact location in museum'), max_length=250, blank=True, null=True)
    donor_name = models.CharField(_('Donor name'), max_length=250, blank=True, null=True)
    display_donor_name = models.BooleanField(_('Display donor name?'), default=False)

    def __str__(self):
        return self.name


class ArtifactImage(models.Model):
    artifact = models.ForeignKey(Artifact, verbose_name=_('Artifact'), on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(_('Image'), upload_to='artifacts/')
    description = models.CharField(_('Description'), max_length=400, blank=True, null=True)
    credit = models.CharField(_('Credit'), max_length=200, blank=True, null=True)
    year_era = models.CharField(_('Year/Era'), max_length=200, blank=True, null=True)
    location = models.CharField(_('Image location'), max_length=200, blank=True, null=True)
    is_cover = models.BooleanField(_('Cover image?'), default=False)

    def __str__(self):
        return f'[{self.id}] {self.artifact.name}'


class ArtifactImageCoord(models.Model):
    image = models.ForeignKey(ArtifactImage, verbose_name=_('Image'), on_delete=models.CASCADE, related_name='coords')
    x = models.CharField(_('X'), max_length=10)
    y = models.CharField(_('Y'), max_length=10)
    width = models.CharField(_('Width'), max_length=10, blank=True, null=True)
    height = models.CharField(_('Height'), max_length=10, blank=True, null=True)
    info = models.CharField(_('Info'), max_length=400, blank=True, null=True)

    def __str__(self):
        return f'[{self.x},{self.y}] {self.image.artifact.name}'
