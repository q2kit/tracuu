import os
import sys
import traceback

import boto3
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = "Backup db.sqlite3 to S3 bucket"

    def handle(self, *args, **options):  # noqa: ARG002
        try:
            # Path to the SQLite database file
            db_path = os.path.join(settings.BASE_DIR, "db.sqlite3")
            if not os.path.exists(db_path):
                msg = f"Database file not found: {db_path}"
                raise FileNotFoundError(msg)  # noqa: TRY301

            # Create a unique backup key using the current timestamp
            now = timezone.localtime().strftime("%Y%m%d_%H%M%S")
            backup_key = f"db_backup/{now}.sqlite3"

            # Get S3 credentials from settings
            endpoint_url = settings.AWS_S3_ENDPOINT_URL
            access_key = settings.AWS_ACCESS_KEY_ID
            secret_key = settings.AWS_SECRET_ACCESS_KEY
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME

            # Create S3 client
            s3 = boto3.client(
                "s3",
                endpoint_url=endpoint_url,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
            )

            # Upload the database file
            with open(db_path, "rb") as f:
                s3.upload_fileobj(f, bucket_name, backup_key)
        except Exception:
            self.stderr.write(f"Backup failed: {traceback.format_exc()}")
            sys.exit(1)
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Backup successful: {backup_key}"),
            )
