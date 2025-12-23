from rest_framework import serializers

from src.models import Receipt


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ["code", "description", "image", "created_at"]
        read_only_fields = ["created_at"]
