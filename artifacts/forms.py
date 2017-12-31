from django import forms
from django.forms import inlineformset_factory, models
from django_countries.widgets import CountrySelectWidget, LazySelectMultiple
from phonenumber_field.formfields import PhoneNumberField

from .models import Artifact, ArtifactImage, OriginArea, ArtifactType, ArtifactMaterial


class ArtifactForm(forms.ModelForm):
    class Meta:
        model = Artifact
        exclude = ['uploaded_at', 'approved_by', 'status', 'is_private', 'acceptance_date', 'origin_city', 'is_displayed', 'displayed_at', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'year_from': forms.TextInput(attrs={'class': 'form-control'}),
            'year_to': forms.TextInput(attrs={'class': 'form-control'}),
            'technical_data': forms.Textarea(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'origin_country': CountrySelectWidget(attrs={'class': 'form-control'}),
            'origin_area': forms.Select(attrs={'class': 'form-control'}),
            'donor_name': forms.TextInput(attrs={'class': 'form-control'}),
            'display_donor_name': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'artifact_type': forms.Select(attrs={'class': 'form-control'}),
            'artifact_materials': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ArtifactForm, self).__init__(*args, **kwargs)
        if self.errors:
            for field in self.fields:
                if field in self.errors:
                    classes = self.fields[field].widget.attrs.get('class', '')
                    classes += ' is-invalid'
                    self.fields[field].widget.attrs['class'] = classes
        # else:
        #     context = super(ArtifactForm, self).get_context_data(**kwargs)
        #     context['artifact'] = self.id


class ArtifactImageForm(forms.ModelForm):
    class Meta:
        model = ArtifactImage
        exclude = ['artifact']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'credit': forms.TextInput(attrs={'class': 'form-control'}),
            'year_era': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'is_cover': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(ArtifactImageForm, self).__init__(*args, **kwargs)
        if self.errors:
            for field in self.fields:
                if field in self.errors:
                    classes = self.fields[field].widget.attrs.get('class', '')
                    classes += ' is-invalid'
                    self.fields[field].widget.attrs['class'] = classes


ArtifactImageFormSet = inlineformset_factory(
    Artifact,
    ArtifactImage,
    form=ArtifactImageForm,
    extra=1,
    can_delete=False
)


class OriginAreaForm(forms.ModelForm):
    class Meta:
        model = OriginArea
        fields = [
            'title',
            'countries'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'countries': LazySelectMultiple(attrs={'class': 'form-control'}),
        }


class UserArtifactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}))
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number is possible also'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Promise not to send spam'}))


class ArtifactFormImages(forms.Form):
    imageDescription = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    imageLocation = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    imageTime = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    photographerName = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
