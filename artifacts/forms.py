from django import forms
from django.forms import inlineformset_factory

from artifacts.models import Artifact, ArtifactImage


class ArtifactForm(forms.ModelForm):
    class Meta:
        model = Artifact
        exclude = ['uploaded_at', 'uploaded_by', 'approved_by', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'technical_data': forms.Textarea(attrs={'rows': '10', 'cols': '1'}),
        }


class UserArtifactForm(ArtifactForm):
    class Meta(ArtifactForm.Meta):
        exclude = ArtifactForm.Meta.exclude + ['is_displayed', 'displayed_at', 'donor_name', 'is_private', 'acceptance_date']


ArtifactImageFormSet = inlineformset_factory(Artifact, ArtifactImage, exclude=('artifact',), extra=1, can_delete=True)