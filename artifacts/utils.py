import os
from uuid import uuid4


def upload_func(instance, filename):
    name, ext = os.path.splitext(filename)
    num = instance.pk if instance.pk else uuid4().hex[:10]
    return '{0}/img_{1}{2}'.format(instance.__class__.__name__.lower(), num, ext.lower())
