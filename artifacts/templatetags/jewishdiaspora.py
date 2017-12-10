from django import template
from django.forms import CheckboxInput, FileInput, RadioSelect, CheckboxSelectMultiple, SelectMultiple, Select
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='addcss')
def addcss(field, given_class):
    existing_classes = field.field.widget.attrs.get('class', None)
    if existing_classes:
        classes = existing_classes + ' ' + given_class
    else:
        classes = given_class
    return field.as_widget(attrs={"class": classes})


@register.filter(name='is_checkbox')
def is_checkbox(field):
    return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__


@register.filter(name='is_file')
def is_file(field):
    return field.field.widget.__class__.__name__ == FileInput().__class__.__name__


@register.filter(name='is_radio')
def is_radio(field):
    return field.field.widget.__class__.__name__ == RadioSelect().__class__.__name__


@register.filter(name='is_checkbox_multi')
def is_checkbox_multi(field):
    return field.field.widget.__class__.__name__ == CheckboxSelectMultiple().__class__.__name__


@register.filter(name='is_select_multi')
def is_select_multi(field):
    return field.field.widget.__class__.__name__ == SelectMultiple().__class__.__name__


@register.filter(name='is_select')
def is_select(field):
    return field.field.widget.__class__.__name__ == Select().__class__.__name__


@register.filter
def boolean_to_icon(arg):
    if arg:
        return mark_safe('<span class="fa fa-check green-icon"></span>')
    else:
        return mark_safe('<span class="fa fa-times red-icon"></span>')
