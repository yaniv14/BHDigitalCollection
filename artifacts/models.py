from django.conf import settings
from django.utils.translation import ugettext as _
from django.db import models
# Create your models here.


STATUSES = ((1, _('Pending Approval')), (2, _('Pending Data')), (3, _('Approved')))


class User(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    phone_number = models.CharField(max_length=15)


class Artifact(models.Model):
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='users', null=True, blank=True)
    added_date = models.DateTimeField()
    acceptance_date = models.DateTimeField()
    status = models.IntegerField(choices=STATUSES)
    private = models.BooleanField()
    name = models.CharField(max_length=500)
    period = models.CharField(max_length=100)
    technical_data = models.CharField(max_length=50)
    story = models.CharField(max_length=500)
    description = models.CharField(max_length=500)


class Image(models.Model):
    path = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    credit = models.CharField(max_length=200)
    period = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE, related_name='images')


