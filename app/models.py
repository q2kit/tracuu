from django.db import models


class Product(models.Model):
    tax_code = models.CharField(max_length=100, unique=True, verbose_name="Mã số thuế")
    product_name = models.CharField(max_length=255, unique=False, verbose_name="Tên sản phẩm")
    image = models.ImageField(upload_to='images/', unique=True, verbose_name="Ảnh mã số thuế")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tax_code

    class Meta:
        ordering = ['-created_at']
