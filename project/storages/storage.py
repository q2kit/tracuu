from django.utils.deconstruct import deconstructible
from storages.backends.s3boto3 import S3Boto3Storage


@deconstructible
class Storage(S3Boto3Storage):
    pass
