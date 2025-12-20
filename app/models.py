from django.core.exceptions import ValidationError
from django.db import models


class Receipt(models.Model):
    code = models.CharField("Mã hóa đơn", max_length=100, unique=True)
    description = models.TextField("Mô tả", default="", blank=True)
    image = models.ImageField("Ảnh")
    created_at = models.DateTimeField("Ngày tạo", auto_now_add=True)
    is_deleted = models.BooleanField("Đã xoá", default=False)

    class Meta:
        verbose_name = "Hóa đơn"
        verbose_name_plural = "Hóa đơn"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.code

    def save(self, *args, **kwargs):
        self.code = self.code.strip().upper()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if Receipt.objects.exclude(id=self.id).filter(code__iexact=self.code).exists():
            raise ValidationError({"code": "Mã hóa đơn đã tồn tại."})
