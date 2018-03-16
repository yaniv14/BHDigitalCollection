import os
from django import template
from django.conf import settings
from django.forms import CheckboxInput, FileInput, RadioSelect, CheckboxSelectMultiple, SelectMultiple, Select
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils import translation
from django.utils.safestring import mark_safe

from artifacts.models import OriginArea

register = template.Library()


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


@register.simple_tag
def svg_icon(icon_name, class_name='', from_upload=False, rtl=False, lang=True):
    if icon_name is None:
        return ''
    result = '<span class="svg-icon {}">'.format(class_name)
    if from_upload:
        file = open(icon_name, 'r')
        result += file.read()
        file.close()
    else:
        if lang:
            result += render_to_string('svgs/{}{}.svg'.format(icon_name, '_he' if rtl else '_en'))
        else:
            result += render_to_string('svgs/{}.svg'.format(icon_name))
    result += '</span>'
    return mark_safe(result)


@register.simple_tag
def bidi(instance, field):
    lang = translation.get_language()[:2]
    return getattr(instance, field + "_" + lang)


@register.simple_tag
def get_base_url(url_name):
    if url_name == 'home':
        return reverse_lazy(url_name)
    return reverse_lazy('artifacts:{}'.format(url_name))


@register.simple_tag
def get_origin_image(origin_id):
    obj = OriginArea.objects.get(pk=int(origin_id))
    return obj.get_image_url()


@register.filter
def bd(instance, field):
    lang = translation.get_language()[:2]
    return getattr(instance, field + "_" + lang)


@register.filter
def get_slug_or_none(artifact):
    if artifact.slug:
        return reverse('artifacts:detail', args=[artifact.slug, ])
    return '#'


@register.filter
def slice_qs(qs, arg):
    return qs[int(arg * 4):int(arg * 4) + 4]


@register.filter
def get_thumb(image, size):
    if not image.image:
        return ''
    if image.has_thumb_size(size):
        return os.path.join(settings.MEDIA_URL, image.get_thumb_path(size))
    return image.image.url


def get_thumb_or_image(image, size):
    if not image.image:
        return ''
    if image.has_thumb_size(size):
        return os.path.join(settings.MEDIA_URL, image.get_thumb_path(size))
    return image.image.url


@register.simple_tag
def private_or_collection_image(artifact):
    if artifact.get_cover_image():
        if artifact.is_private:
            return artifact.get_cover_image().image.url
        else:
            return get_thumb_or_image(artifact.get_cover_image(), 'small_thumbnail_vertical')
    return ''
