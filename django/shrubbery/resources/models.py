import os

from django.conf import settings
from django.db import models


class Resource(models.Model):

    content = models.FileField(upload_to='resources')

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.content.path))
        super(Resource, self).delete(*args, **kwargs)
