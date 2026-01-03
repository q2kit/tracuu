from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Collate
from django.utils import timezone

from src.const import CODE_MAX_LENGTH
from src.funcs import generate_presigned_url


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

    def image_url_custom_expiry(self, expire_seconds: int = 60 * 3) -> str | None:
        if self.image:
            return generate_presigned_url(
                object_key=f"images/{self.image.name}",
                expire_seconds=expire_seconds,
            )
        return None

    @property
    def is_recent(self) -> bool:
        return self.created_at >= timezone.now() - timezone.timedelta(hours=24)
