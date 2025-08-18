import os
import sys

import boto3
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = "Backup db.sqlite3 to R2 bucket"

    def handle(self, *args, **options):  # noqa: ARG002
        db_path = os.path.join(settings.BASE_DIR, "db.sqlite3")
        if not os.path.exists(db_path):
            self.stderr.write(f"Database file not found: {db_path}")
            sys.exit(1)

        now = timezone.localtime().strftime("%Y%m%d_%H%M%S")
        backup_key = f"db_backup/{now}.sqlite3"

        # Get R2/S3 credentials from settings
        endpoint_url = settings.AWS_S3_ENDPOINT_URL
        access_key = settings.AWS_ACCESS_KEY_ID
        secret_key = settings.AWS_SECRET_ACCESS_KEY
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        region_name = settings.AWS_S3_REGION_NAME

        # Create S3 client for R2
        s3 = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region_name,
        )

        try:
            with open(db_path, "rb") as f:
                s3.upload_fileobj(f, bucket_name, backup_key)
            self.stdout.write(self.style.SUCCESS(f"Backup successful: {backup_key}"))
        except Exception as e:
            self.stderr.write(f"Backup failed: {e}")
            sys.exit(1)
