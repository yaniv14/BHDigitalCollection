from django import forms
from django.forms import inlineformset_factory

from artifacts.models import Artifact, ArtifactImage







class ArtifactForm(forms.ModelForm):
    class Meta:
        model = Artifact
        fields = []
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'technical_data': forms.Textarea(attrs={'rows': '10', 'cols': '1'}),
        }



# class UserArtifactForm(ArtifactForm):
#     class Meta(ArtifactForm.Meta):
#         exclude = ArtifactForm.Meta.exclude + ['is_displayed', 'displayed_at', 'donor_name', 'is_private', 'acceptance_date']
#



class ArtifactFormPersonDetails(forms.ModelForm):
    class Meta(ArtifactForm.Meta):
        fields = ArtifactForm.Meta.fields+['donor_name', 'donor_phone_prefix','donor_phone_number', 'mail']



class ArtifactFormArtifactDetails(forms.ModelForm):
    class Meta(ArtifactForm.Meta):
        fields = ArtifactForm.Meta.fields+['artifact_name', 'origin_city', 'origin_country', 'origin_area',
                                           'description', 'short_description', 'category', 'technical_data', ]

class ArtifactFormArtifactPictures(forms.ModelForm):
    class Meta(ArtifactForm.Meta):
        fields = ArtifactForm.Meta.fields+[]



ArtifactImageFormSet = inlineformset_factory(Artifact, ArtifactImage, exclude=('artifact',), extra=1, can_delete=True)