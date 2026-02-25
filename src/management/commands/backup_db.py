import os
import sys
import traceback

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from src.funcs import upload_file_to_s3


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

            # Upload the database file
            upload_file_to_s3(db_path, backup_key)
        except Exception:
            self.stderr.write(f"Backup failed: {traceback.format_exc()}")
            sys.exit(1)
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Backup successful: {backup_key}"),
            )
