import os
from uuid import uuid4

from PIL import Image


def upload_func(instance, filename):
    name, ext = os.path.splitext(filename)
    num = instance.pk if instance.pk else uuid4().hex[:10]
    return '{0}/img_{1}{2}'.format(instance.__class__.__name__.lower(), num, ext.lower())


def get_cropped_image(image_data, image_type, width, height):
    picture = image_data.image.image
    image = Image.open(picture)
    json_data = getattr(image_data, image_type)
    cropped_image = image.crop((
        json_data.get('x'),
        json_data.get('y'),
        float(json_data.get('w')) + float(json_data.get('x')),
        float(json_data.get('h')) + float(json_data.get('y'))
    ))
    resized_image = cropped_image.resize((int(width), int(height)), Image.ANTIALIAS)
    resized_image.save(picture.file.path)

    return resized_image
