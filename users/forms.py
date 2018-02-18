from authtools.forms import AuthenticationForm
from django import forms
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from bhdigitalcollection.fields import ILPhoneNumberMultiWidget
from .models import ArtifactContact


class ContactForm(forms.ModelForm):
    class Meta:
        model = ArtifactContact
        exclude = ['submitted_at', ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'artifact_info': forms.Textarea(attrs={'class': 'form-control'}),
            'intend_type': forms.Select(attrs={'class': 'form-control'}),
        }

    def send_email(self):
        data = self.cleaned_data

        return send_mail(
            _('Artifact contact form'),
            f'Name: {data["name"]}\n'
            f'Email: {data["email"]}\n'
            f'Phone: {data["phone"]}\n'
            f'Artifact info: {data["artifact_info"]}\n'
            f'Intend to: {data["intend_type"]}',
            data['email'],
            ['yanivmirel@gmail.com'],
            fail_silently=False,
        )


class LoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super(LoginForm, self).__init__(request, *args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'

        if self.errors:
            for field in self.fields:
                if field in self.errors:
                    classes = self.fields[field].widget.attrs.get('class', '')
                    classes += ' is-invalid'
                    self.fields[field].widget.attrs['class'] = classes


class MyUserAccount(forms.Form):
    full_name = forms.CharField(label=_('First and last name'), max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': _('First and last name')
        }
    ))
    phone_number = forms.CharField(label=_('Phone number'), widget=ILPhoneNumberMultiWidget(
        area_attrs={'class': 'form-control'},
        number_attrs={'class': 'form-control', 'size': '7', 'maxlength': '7', 'placeholder': _('Mobile preferred')},
    ))
    email = forms.EmailField(
        label=_('Email address'),
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('We will never send you spam')
            }
        ))
    password = forms.CharField(
        label=_('Password'),
        max_length=30,
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password')
            }
        ))
    password2 = forms.CharField(
        label=_('Verify Password'),
        max_length=30,
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password')
            }
        ))

    def __init__(self, *args, **kwargs):
        self.logged = kwargs.pop('logged')
        bidi = kwargs.pop('bidi')
        super(MyUserAccount, self).__init__(*args, **kwargs)
        self.fields['phone_number'].widget = ILPhoneNumberMultiWidget(
            bidi=bidi,
            area_attrs={'class': 'form-control'},
            number_attrs={'class': 'form-control', 'size': '7', 'maxlength': '7', 'placeholder': _('Mobile preferred')},
        )

    def clean_password2(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError(
                _("The passwords are not equal"),
                code='invalid'
            )
        return password2
