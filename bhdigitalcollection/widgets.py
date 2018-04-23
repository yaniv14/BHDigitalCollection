from django.forms.widgets import ChoiceWidget, CheckboxSelectMultiple, RadioSelect


class OriginRadioSelect(ChoiceWidget):
    input_type = 'radio'
    template_name = 'originradio.html'
    option_template_name = 'originradio_option.html'


class MaterialCheckboxSelectMultiple(CheckboxSelectMultiple):
    template_name = 'material_checkbox_select.html'
    option_template_name = 'material_checkbox_option.html'


class ArtifactTypeRadioSelect(RadioSelect):
    template_name = 'type_radio_select.html'
    option_template_name = 'type_radio_option.html'
