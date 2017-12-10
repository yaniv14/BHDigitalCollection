from django import forms
from artifacts.models import Artifact


class ArtifactForm(forms.ModelForm):
    class Meta:
        model = Artifact
        exclude = ['uploaded_at', 'uploaded_by', 'approved_by', 'status']


class UserArtifactForm(ArtifactForm):
    class Meta(ArtifactForm.Meta):
        exclude = ArtifactForm.Meta.exclude + ['is_displayed', 'displayed_at', 'donor_name', 'is_private', 'acceptance_date']