import os
from PIL import Image
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core.validators import validate_image_file_extension
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django_countries.fields import CountryField

from artifacts.utils import upload_func


class ArtifactStatus(object):
    PENDING = 1
    MISSING = 2
    APPROVED = 3
    REJECTED = 4
    DISABLED = 5

    choices = (
        (PENDING, _('Pending approval')),
        (MISSING, _('Missing info')),
        (APPROVED, _('Approved')),
        (REJECTED, _('Rejected')),
        (DISABLED, _('Disabled')),
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
    title_he = models.CharField(_('Title Hebrew'), max_length=250)
    title_en = models.CharField(_('Title English'), max_length=250)
    image = models.ImageField(_('Image'), upload_to=upload_func, blank=True, null=True,
                              validators=[validate_image_file_extension])

    def __str__(self):
        return self.title_he if self.title_he else self.title_en


class ArtifactMaterial(models.Model):
    title_he = models.CharField(_('Title Hebrew'), max_length=250)
    title_en = models.CharField(_('Title English'), max_length=250)

    def __str__(self):
        return self.title_he if self.title_he else self.title_en


class OriginArea(models.Model):
    title_he = models.CharField(_('Title Hebrew'), max_length=250)
    title_en = models.CharField(_('Title English'), max_length=250)
    countries = CountryField(_('Country'), multiple=True, blank=True)
    image = models.ImageField(_('Background image'), upload_to=upload_func, blank=True, null=True,
                              validators=[validate_image_file_extension])

    def __str__(self):
        return self.title_he if self.title_he else self.title_en

    def get_image_url(self):
        if self.image:
            return self.image.url
        return ''

    def get_countries_list(self):
        return [
            {
                'name': x.name,
                'code': x.code,
                'flag': x.flag
            } for x in self.countries
        ]

    def get_artifacts_count(self):
        return self.artifacts.count()


class Artifact(models.Model):
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                    related_name='uploaded_artifacts', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                    related_name='approved_artifacts', null=True, blank=True)
    artifact_type = models.ForeignKey(ArtifactType, verbose_name=_('Artifact type'), on_delete=models.SET_NULL,
                                      related_name='artifacts', null=True, blank=True)
    artifact_materials = models.ManyToManyField(ArtifactMaterial, verbose_name=_('Artifact material'),
                                                related_name='artifacts', blank=True)
    status = models.PositiveSmallIntegerField(_('Status'), choices=ArtifactStatus.choices,
                                              default=ArtifactStatus.PENDING)
    is_private = models.BooleanField(_('Privately owned artifact'), default=False)
    is_featured = models.BooleanField(_('Featured'), default=False)
    item_no = models.CharField(_('Item No'), max_length=250, blank=True)
    name_he = models.CharField(_('Name Hebrew'), max_length=250)
    name_en = models.CharField(_('Name English'), max_length=250)
    slug = models.SlugField(_('Slug'), max_length=250, allow_unicode=True, blank=True)
    year_from = models.IntegerField(_('Year from'), blank=True, null=True)
    year_to = models.IntegerField(_('Year to'), blank=True, null=True)
    technical_data_he = models.TextField(_('Technical data Hebrew'), blank=True, null=True)
    technical_data_en = models.TextField(_('Technical data English'), blank=True, null=True)
    description_he = models.TextField(_('Description Hebrew'), blank=True, null=True)
    description_en = models.TextField(_('Description English'), blank=True, null=True)
    origin_city_he = models.CharField(_('City Hebrew'), max_length=100, blank=True, null=True)
    origin_city_en = models.CharField(_('City English'), max_length=100, blank=True, null=True)
    origin_country = CountryField(_('Country'), blank=True, null=True)
    origin_area = models.ForeignKey(OriginArea, verbose_name=_('Area'), on_delete=models.SET_NULL, blank=True,
                                    null=True, related_name='artifacts')
    is_displayed = models.BooleanField(_('Displayed in museum?'), default=False)
    displayed_at_he = models.CharField(_('Artifact location in museum Hebrew'), max_length=250, blank=True, null=True)
    displayed_at_en = models.CharField(_('Artifact location in museum English'), max_length=250, blank=True, null=True)
    donor_name_he = models.CharField(_('Donor name Hebrew'), max_length=250, blank=True, null=True)
    donor_name_en = models.CharField(_('Donor name English'), max_length=250, blank=True, null=True)
    credit_he = models.CharField(_('Artifact credit Hebrew'), max_length=500, blank=True)
    credit_en = models.CharField(_('Artifact credit English'), max_length=500, blank=True)
    display_donor_name = models.BooleanField(_('Display donor name?'), default=False)
    route_map = models.ImageField(_('Artifact route map'), upload_to=upload_func, blank=True, null=True,
                                  validators=[validate_image_file_extension])
    route_he = models.CharField(_('Artifact route Hebrew'), max_length=500, blank=True, null=True)
    route_en = models.CharField(_('Artifact route English'), max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name_he if self.name_he else self.name_en

    def get_years(self):
        if self.year_from:
            if self.year_to:
                if self.year_from == self.year_to:
                    return '{}-{}'.format(self.year_from, self.year_to)
            return self.year_from
        elif self.year_to:
            return self.year_to
        return None

    def get_all_tags(self):
        artifact_type = [self.artifact_type.title_he] if self.artifact_type else []
        artifact_materials = [x.title_he for x in self.artifact_materials.all()]
        artifact_origin = [self.origin_country.name] if self.origin_country else []
        return artifact_materials + artifact_type + artifact_origin

    def get_cover_image(self):
        image = self.images.filter(is_cover=True).first()
        if image:
            return image
        # Fallback to not cover image
        image = self.images.filter(is_cover=False).first()
        if image:
            return image

        return None


THUMBNAIL_TYPES = {
    'small_thumbnail': [240, 240],
    'small_thumbnail_vertical': [240, 300],
    'big_thumbnail': [540, 540],
    'cover': [1920, 690],
    'footer': [1920, 240],
}


class ArtifactImage(models.Model):
    artifact = models.ForeignKey(Artifact, verbose_name=_('Artifact'), on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(_('Image'), upload_to=upload_func, validators=[validate_image_file_extension])
    description_he = models.CharField(_('Description Hebrew'), max_length=400, blank=True, null=True)
    description_en = models.CharField(_('Description English'), max_length=400, blank=True, null=True)
    credit_he = models.CharField(_('Credit Hebrew'), max_length=200, blank=True, null=True)
    credit_en = models.CharField(_('Credit English'), max_length=200, blank=True, null=True)
    year_era_he = models.CharField(_('Year/Era Hebrew'), max_length=200, blank=True, null=True)
    year_era_en = models.CharField(_('Year/Era English'), max_length=200, blank=True, null=True)
    location_he = models.CharField(_('Image location Hebrew'), max_length=200, blank=True, null=True)
    location_en = models.CharField(_('Image location English'), max_length=200, blank=True, null=True)
    is_cover = models.BooleanField(_('Cover image?'), default=False)
    thumbnails = JSONField(verbose_name=_('Small thumbnail square'), blank=True, null=True)

    def __str__(self):
        return f'[{self.id}] {self.artifact.name_he}'

    def has_thumb_size(self, size):
        if not self.thumbnails:
            return False
        return True if self.thumbnails.get(size) else False

    def get_thumb_path(self, k):
        name, ext = os.path.splitext(self.image.name)
        path, image_name = os.path.split(name)
        if not os.path.exists(f"{path}/CACHE"):
            os.makedirs(f"{path}/CACHE")
        return f"{path}/CACHE/{image_name}_{k}{ext}"

    def generate_thumbnails(self):
        for k, size in THUMBNAIL_TYPES.items():
            box = self.thumbnails.get(k)
            if not box:
                continue
            im = Image.open(self.image.file)
            piece = im.crop(box)
            piece = piece.resize(size)
            new_path = os.path.join(settings.MEDIA_ROOT, self.get_thumb_path(k))
            piece.save(new_path)


class ArtifactImageCoord(models.Model):
    image = models.ForeignKey(ArtifactImage, verbose_name=_('Image'), on_delete=models.CASCADE, related_name='coords')
    x = models.CharField(_('X'), max_length=10)
    y = models.CharField(_('Y'), max_length=10)
    width = models.CharField(_('Width'), max_length=10, blank=True, null=True)
    height = models.CharField(_('Height'), max_length=10, blank=True, null=True)
    info_he = models.CharField(_('Info'), max_length=400, blank=True, null=True)
    info_en = models.CharField(_('Info'), max_length=400, blank=True, null=True)

    def __str__(self):
        return f'[{self.x},{self.y}] {self.image.artifact.name_he}'


class PageBanner(models.Model):
    page = models.CharField(_('Page'), max_length=250, choices=Pages.choices, blank=True, null=True)
    image = models.ImageField(_('Image'), upload_to=upload_func, validators=[validate_image_file_extension])
    main_text_he = models.CharField(_('Main text Hebrew'), max_length=400, blank=True, null=True)
    main_text_en = models.CharField(_('Main text English'), max_length=400, blank=True, null=True)
    description_he = models.CharField(_('Description Hebrew'), max_length=400, blank=True, null=True)
    description_en = models.CharField(_('Description English'), max_length=400, blank=True, null=True)
    credit_he = models.CharField(_('Credit Hebrew'), max_length=200, blank=True, null=True)
    credit_en = models.CharField(_('Credit English'), max_length=200, blank=True, null=True)
    active = models.BooleanField(_('Active?'), default=True)

    def __str__(self):
        return f'[{self.id}] {self.get_page_display()}'
