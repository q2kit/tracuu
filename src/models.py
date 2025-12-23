from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Collate


class Receipt(models.Model):
    code = models.CharField(
        "Mã hóa đơn",
        max_length=100,
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

    def clean(self):
        super().clean()
        if Receipt.objects.exclude(id=self.id).filter(code__iexact=self.code).exists():
            raise ValidationError({"code": "Mã hóa đơn đã tồn tại."})

    def delete(self, *args, **kwargs):  # noqa: ARG002
        self.is_deleted = True
        self.save(update_fields=["is_deleted"])
