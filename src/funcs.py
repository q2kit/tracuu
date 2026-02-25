import boto3
import requests
from django.conf import settings

from src.const import (
    NORMAL_IMAGE_EXPIRY_SECONDS,
    SERVER_HOST,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
)


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


def upload_file_to_s3(file_name: str, upload_name: str) -> None:
    s3_client = boto3.client(
        "s3",
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        region_name=settings.AWS_S3_REGION_NAME,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    s3_client.upload_file(
        Filename=file_name,
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=upload_name,
    )


def download_file_from_s3(object_key: str, download_path: str) -> None:
    s3_client = boto3.client(
        "s3",
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        region_name=settings.AWS_S3_REGION_NAME,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    s3_client.download_file(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=object_key,
        Filename=download_path,
    )


def receipt_created_notify(receipt):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    caption = "\n".join(
        [
            f"Code: {receipt.code}",
            f"Description: {receipt.description}" if receipt.description else "",
            f"URL: https://{SERVER_HOST}?code={receipt.code}",
        ],
    )
    photo = receipt.image_url_custom_expiry()
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "caption": caption,
        "photo": photo,
    }
    requests.post(url, data=data, timeout=5)
