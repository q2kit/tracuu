import re

from PIL import Image
from rest_framework import serializers

from src.const import CODE_MAX_LENGTH, IMAGE_ALLOWED_TYPES, IMAGE_MAX_SIZE_MB
from src.models import Receipt


class ReceiptSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=False)
    image_name = serializers.CharField(source="image.name", read_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)
    is_deleted = serializers.BooleanField(write_only=True, required=False, default=False)
    is_recent = serializers.BooleanField(read_only=True)

    class Meta:
        model = Receipt
        fields = [
            "id",
            "code",
            "description",
            "image",
            "image_name",
            "image_url",
            "is_deleted",
            "is_recent",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_code(self, value):
        value = value.strip().upper()
        pattern = re.compile(r"^[A-Z0-9\-_]+$", re.IGNORECASE)
        error_msg = None
        if not pattern.match(value):
            error_msg = (
                "Mã hóa đơn chỉ được chứa chữ cái, số, dấu gạch ngang và dấu gạch dưới."
            )
        elif len(value) > CODE_MAX_LENGTH:
            error_msg = "Mã hóa đơn không được vượt quá 100 ký tự."
        else:
            qs = Receipt.objects.filter(code__iexact=value, is_deleted=False)
            if self.instance:
                qs = qs.exclude(id=self.instance.id)
            if qs.exists():
                error_msg = "Mã hóa đơn đã tồn tại."
        if error_msg:
            raise serializers.ValidationError(error_msg)
        return value

    def validate_image(self, value):
        if value.size > IMAGE_MAX_SIZE_MB * 1024 * 1024:
            msg = f"Kích thước ảnh không được vượt quá {IMAGE_MAX_SIZE_MB} MB."
            raise serializers.ValidationError(msg)
        if value.content_type not in IMAGE_ALLOWED_TYPES:
            msg = "Định dạng ảnh không hợp lệ. Vui lòng tải lên ảnh hợp lệ."
            raise serializers.ValidationError(msg)

        # Validate actual file content using Pillow to prevent spoofed MIME types
        try:
            # Open and verify the image
            img = Image.open(value)
            img.verify()  # Verify that it is, in fact, an image
            # Reset file pointer and reopen to get format after verify()
            value.seek(0)
            img = Image.open(value)
            img_format = img.format.lower() if img.format else None
        except Exception:
            msg = "File tải lên không phải là ảnh hợp lệ."
            raise serializers.ValidationError(msg) from None

        # Check if the actual image format matches allowed types
        allowed_formats = {"jpeg", "jpg", "png", "gif", "webp"}
        if img_format not in allowed_formats:
            msg = "Định dạng ảnh không hợp lệ. Vui lòng tải lên ảnh hợp lệ."
            raise serializers.ValidationError(msg)

        return value

    def get_image_url(self, obj):
        if expire_seconds := self.context.get("image_expire_seconds"):
            return obj.custom_image_url(expire_seconds=expire_seconds)
        return obj.image.url
