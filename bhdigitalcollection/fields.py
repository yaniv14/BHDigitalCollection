from django import forms
from django.utils.translation import ugettext_lazy as _
from django_countries.data import COUNTRIES
from django_countries.widgets import CountrySelectWidget

from artifacts.models import OriginArea


class ILPhoneNumberMultiWidget(forms.MultiWidget):
    """
    A Widget that splits IL Phone number input into <input type='text'> and <select> boxes.
    """
    template_name = 'ilphonenumber.html'

    def __init__(self, attrs=None, area_attrs=None, number_attrs=None, bidi=False):

        IL_AREA_CODE = (
            ('', _('Area code')),
            ('02', '02'),
            ('03', '03'),
            ('04', '04'),
            ('050', '050'),
            ('052', '052'),
            ('053', '053'),
            ('054', '054'),
            ('055', '055'),
            ('057', '057'),
            ('058', '058'),
            ('072', '072'),
            ('073', '073'),
            ('076', '076'),
            ('077', '077'),
            ('079', '079'),
            ('08', '08'),
            ('09', '09'),
        )
        if bidi:
            widgets = (
                forms.TextInput(
                    attrs=attrs if number_attrs is None else number_attrs
                ),
                forms.Select(
                    attrs=attrs if area_attrs is None else area_attrs,
                    choices=IL_AREA_CODE
                ),
            )
        else:
            widgets = (
                forms.Select(
                    attrs=attrs if area_attrs is None else area_attrs,
                    choices=IL_AREA_CODE
                ),
                forms.TextInput(
                    attrs=attrs if number_attrs is None else number_attrs
                ),
            )
        super().__init__(widgets)
        self.bidi = bidi

    def decompress(self, value):
        if value:
            if self.bidi:
                return value.split('-')[::-1]  # reverse order base on form location
            return value.split('-')
        return [None, None]

    def value_from_datadict(self, data, files, name):
        values = super(ILPhoneNumberMultiWidget, self).value_from_datadict(data, files, name)
        for d in filter(lambda x: x.startswith(name), data):
            index = int(d[len(name) + 1:])
            values[index] = data[d]
        if values[0] == values[1] == '':
            return None
        if self.bidi:
            return '%s-%s' % tuple(values)[::-1]  # reverse order base on form location
        return '%s-%s' % tuple(values)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['bidi'] = self.bidi
        return context


class CountryOrAreaMultiWidget(forms.MultiWidget):
    template_name = 'country_area.html'

    def __init__(
            self,
            attrs=None,
            country_attrs=None,
            country_radio_attrs=None,
            area_radio_attrs=None,
            area_attrs=None):
        widgets = (
            forms.CheckboxInput(
                attrs=attrs if country_radio_attrs is None else country_radio_attrs
            ),

            CountrySelectWidget(
                choices=((k, v) for k, v in COUNTRIES.items()),
                attrs=attrs if country_attrs is None else country_attrs),

            forms.CheckboxInput(attrs=attrs if area_radio_attrs is None else area_radio_attrs),

            forms.Select(
                attrs=attrs if area_attrs is None else area_attrs,
                choices=[('', _('Area or continent'))] + [(x.id, x.title_he) for x in OriginArea.objects.all()]
            )
        )
        super().__init__(widgets)

    def decompress(self, value):
        if value:
            return value
        return [None, None, None, None]


class PeriodMultiWidget(forms.MultiWidget):
    template_name = 'period.html'

    def __init__(
            self,
            attrs=None,
            year_from_attrs=None,
            year_to_attrs=None,
            period_attrs=None,
            exact_year_radio_attrs=None,
            exact_year_attrs=None):
        widgets = (
            forms.CheckboxInput(
                attrs=attrs if period_attrs is None else period_attrs
            ),

            forms.TextInput(
                attrs=attrs if year_from_attrs is None else year_from_attrs
            ),

            forms.TextInput(
                attrs=attrs if year_to_attrs is None else year_to_attrs
            ),

            forms.CheckboxInput(
                attrs=attrs if exact_year_radio_attrs is None else exact_year_radio_attrs
            ),

            forms.TextInput(
                attrs=attrs if exact_year_attrs is None else exact_year_attrs
            )
        )
        super().__init__(widgets)

    def decompress(self, value):
        if value:
            return value
        return [True, '', '', False, '']
