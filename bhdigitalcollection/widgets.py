from django.forms.widgets import ChoiceWidget


class OriginRadioSelect(ChoiceWidget):
    input_type = 'radio'
    template_name = 'originradio.html'
    option_template_name = 'originradio_option.html'
