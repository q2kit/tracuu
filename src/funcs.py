import boto3
from django.conf import settings

from src.const import NORMAL_IMAGE_EXPIRY_SECONDS


def generate_presigned_url(
    *,
    bucket_name: str = settings.AWS_STORAGE_BUCKET_NAME,
    object_key: str,
    expire_seconds: int = NORMAL_IMAGE_EXPIRY_SECONDS,
) -> str:
    s3_client = boto3.client(
        "s3",
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        region_name=settings.AWS_S3_REGION_NAME,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": object_key},
        ExpiresIn=expire_seconds,
    )
