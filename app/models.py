from django.db import models


class Product(models.Model):
    tax_code = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Mã số thuế",
    )
    product_name = models.CharField(
        max_length=255,
        verbose_name="Tên sản phẩm",
    )
    image = models.ImageField(
        upload_to="images/",
        verbose_name="Ảnh mã số thuế",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.tax_code
