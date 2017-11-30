from django.db import models
from authtools.models import AbstractEmailUser
from django.utils.translation import ugettext as _


class User(AbstractEmailUser):
    full_name = models.CharField(_('Full name'), max_length=255, blank=True)
    phone = models.CharField(_('Phone'), max_length=255, blank=True)

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name