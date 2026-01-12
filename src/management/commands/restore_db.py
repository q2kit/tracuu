import os
import sys
import traceback

from django.conf import settings
from django.core.management.base import BaseCommand

from src.funcs import download_file_from_s3


class Command(BaseCommand):
    help = "Restore db.sqlite3 from S3 bucket"

    def add_arguments(self, parser):
        parser.add_argument("db_filename", type=str, help="S3 DB object key")

    def handle(self, *args, **options):  # noqa: ARG002
        db_filename = options["db_filename"]
        db_path = os.path.join(settings.BASE_DIR, "db.sqlite3")
        try:
            download_file_from_s3(db_filename, db_path)
        except Exception:
            self.stderr.write(f"Restore failed: {traceback.format_exc()}")
            sys.exit(1)
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Restore successful: {db_filename} -> {db_path}",
                ),
            )
