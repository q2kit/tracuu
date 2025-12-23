from django.contrib import admin
from django.contrib.auth.models import Group

from src.models import Receipt

admin.site.site_header = "Tra cứu hoá đơn 24/7"
admin.site.site_title = "Tra cứu hoá đơn 24/7"


class ReceiptAdmin(admin.ModelAdmin):
    search_fields = ["code", "description"]
    list_display = ["code", "description", "image", "created_at"]
    fields = ["code", "description", "image"]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_deleted=False)

    def delete_model(self, request, obj):  # noqa: ARG002
        obj.is_deleted = True
        obj.save(update_fields=["is_deleted"])

    def delete_queryset(self, request, queryset):  # noqa: ARG002
        queryset.update(is_deleted=True)


admin.site.register(Receipt, ReceiptAdmin)

admin.site.unregister(Group)
