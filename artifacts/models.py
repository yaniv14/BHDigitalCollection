from django.conf import settings
from django.utils.translation import ugettext as _
from django.db import models
from django_countries.fields import CountryField
from taggit.managers import TaggableManager


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


class Pages(object):
    MUSEUM_COLLECTIONS = 'museum_collections'
    USERS_COLLECTIONS = 'users_collections'
    ALL_COLLECTIONS = 'all_collections'
    ABOUT = 'about'
    CONTACT = 'contact'
    ACCOUNT = 'account'
    LOGIN = 'login'
    UPLOAD_STEP_1 = 'upload_step_1'
    UPLOAD_STEP_2 = 'upload_step_2'
    UPLOAD_STEP_3 = 'upload_step_3'

    choices = (
        (MUSEUM_COLLECTIONS, _('Museum collections')),
        (USERS_COLLECTIONS, _('Users collections')),
        (ALL_COLLECTIONS, _('All collections')),
        (ABOUT, _('About')),
        (CONTACT, _('Contact')),
        (ACCOUNT, _('Account')),
        (LOGIN, _('Login')),
        (UPLOAD_STEP_1, _('Upload step 1')),
        (UPLOAD_STEP_2, _('Upload step 2')),
        (UPLOAD_STEP_3, _('Upload step 3')),
    )


class ArtifactType(models.Model):
    title = models.CharField(_('Title'), max_length=250)

    def __str__(self):
        return self.title


class ArtifactMaterial(models.Model):
    title = models.CharField(_('Title'), max_length=250)

    def __str__(self):
        return self.title


class Artifact(models.Model):
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                    related_name='uploaded_artifacts', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    acceptance_date = models.DateTimeField(blank=True, null=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                    related_name='approved_artifacts', null=True, blank=True)
    artifact_type = models.ForeignKey(ArtifactType, verbose_name=_('Artifact type'), on_delete=models.SET_NULL,
                                      related_name='artifacts', null=True, blank=True)
    artifact_materials = models.ManyToManyField(ArtifactMaterial, verbose_name=_('Artifact material'),
                                                related_name='artifacts', blank=True)
    status = models.PositiveSmallIntegerField(_('Status'), choices=ArtifactStatus.choices,
                                              default=ArtifactStatus.PENDING)
    is_private = models.BooleanField(_('Privately owned artifact'), default=False)
    name = models.CharField(_('Name'), max_length=250)
    year_era = models.CharField(_('Era/Years range'), max_length=200)
    technical_data = models.TextField(_('Technical data'))
    description = models.TextField(_('Description'))
    origin_city = models.CharField(_('City'), max_length=100, blank=True, null=True)
    origin_country = CountryField(_('Country'), blank=True, null=True)
    origin_area = models.CharField(_('Area'), max_length=250, blank=True, null=True)
    is_displayed = models.BooleanField(_('Displayed in museum?'), default=False)
    displayed_at = models.CharField(_('Artifact location in museum'), max_length=250, blank=True, null=True)
    donor_name = models.CharField(_('Donor name'), max_length=250, blank=True, null=True)
    display_donor_name = models.BooleanField(_('Display donor name?'), default=False)

    def __str__(self):
        return self.name

    def get_cover_image(self):
        image = self.images.filter(is_cover=True).first()
        if image:
            return image.image

        # return some default image instead
        return None


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


class PageBanner(models.Model):
    page = models.CharField(_('Page'), max_length=250, choices=Pages.choices, blank=True, null=True)
    image = models.ImageField(_('Image'), upload_to='banners/')
    main_text = models.CharField(_('Main text'), max_length=400, blank=True, null=True)
    description = models.CharField(_('Description'), max_length=400, blank=True, null=True)
    credit = models.CharField(_('Credit'), max_length=200, blank=True, null=True)
    active = models.BooleanField(_('Active?'), default=True)

    def __str__(self):
        return f'[{self.id}] {self.get_page_display()}'
