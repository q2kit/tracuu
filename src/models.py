import time

from django.conf import settings
from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Collate
from django.utils import timezone

from src.const import CODE_MAX_LENGTH, SERVER_HOST


class Receipt(models.Model):
    code = models.CharField(
        "Mã hóa đơn",
        max_length=CODE_MAX_LENGTH,
    )
    description = models.TextField("Mô tả", default="", blank=True)
    image = models.ImageField("Ảnh")
    created_at = models.DateTimeField("Ngày tạo", auto_now_add=True)
    is_deleted = models.BooleanField("Đã xóa", default=False)

    class Meta:
        db_table = "receipts"
        verbose_name = "Hóa đơn"
        verbose_name_plural = "Hóa đơn"
        ordering = ["-created_at"]
        constraints = [
            UniqueConstraint(
                Collate("code", "NOCASE"),
                condition=models.Q(is_deleted=False),
                name="uniq_receipt_code_nocase",
            ),
        ]

    def __str__(self) -> str:
        return self.code

    def save(self, *args, **kwargs):
        self.code = self.code.strip().upper()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):  # noqa: ARG002
        self.is_deleted = True
        self.save(update_fields=["is_deleted"])

    @property
    def detail_url(self) -> str:
        scheme = "http" if settings.DEBUG else "https"
        timestamp = int(time.time())
        return f"{scheme}://{SERVER_HOST}?code={self.code}&t={timestamp}"

    @property
    def is_recent(self) -> bool:
        return self.created_at >= timezone.now() - timezone.timedelta(hours=24)
