from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from django.utils.deconstruct import deconstructible
from storages.backends.s3boto3 import S3Boto3Storage


@deconstructible
class ImageStorage(S3Boto3Storage):
    pass


@deconstructible
class StaticStorage(ManifestStaticFilesStorage):
    pass
