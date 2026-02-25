import re
from pathlib import Path

from concurrent_log_handler import ConcurrentTimedRotatingFileHandler

from src.funcs import upload_file_to_s3


class S3ConcurrentTimedRotatingFileHandler(ConcurrentTimedRotatingFileHandler):
    def __init__(self, *args, **kwargs) -> None:
        self.dirName = Path(kwargs.get("filename")).resolve().parent
        self.s3_log_prefix = "logs/"
        if not self.dirName.exists():
            self.dirName.mkdir(parents=True, exist_ok=True)
        super().__init__(*args, **kwargs)
        self.suffix = "%Y%m%d_%H%M"  # override
        self.extMatch = re.compile(r"^\d{4}\d{2}\d{2}_\d{2}\d{2}.log$", re.ASCII)

    def rotation_filename(self, default_name: str):
        """
        description:
            Modify the filename of a log file when rotating.
        param:
            default_name: The default name for the log file.
            example-> /logs/general.log.20250131_1200
        return:
            /logs/20250131_1200.log
        """
        suffix = default_name.rsplit(".", maxsplit=1)[-1]
        return f"{self.dirName / suffix}.log"

    def getListOfFiles(self):  # noqa: N802
        return sorted(
            [
                file
                for file in self.dirName.iterdir()
                if self.extMatch.match(str(file.name))
            ],
        )

    def doRollover(self):  # noqa: N802
        super().doRollover()
        latest_file = self.getListOfFiles()[-1]
        upload_file_to_s3(
            file_name=str(latest_file),
            upload_name=f"{self.s3_log_prefix}{latest_file.name}",
        )

    def getFilesToDelete(self):  # noqa: N802
        """
        description:
            Determine the files to delete when rolling over.
        """
        files = self.getListOfFiles()
        if len(files) < self.backupCount:
            return []
        return files[: -self.backupCount]
