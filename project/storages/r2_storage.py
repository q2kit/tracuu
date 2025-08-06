import os
import uuid

from django.utils.deconstruct import deconstructible
from storages.backends.s3boto3 import S3Boto3Storage


@deconstructible
class R2Storage(S3Boto3Storage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            base, ext = os.path.splitext(os.path.basename(name))
            dir_name = os.path.dirname(name)
            new_name = f"{base}_{uuid.uuid4().hex}{ext}"
            name = os.path.join(dir_name, new_name)
        return super().get_available_name(name, max_length=max_length)
