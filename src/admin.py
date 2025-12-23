from django.contrib import admin
from django.contrib.auth.models import Group

from src.models import Receipt

admin.site.site_header = "Tra cứu hoá đơn 24/7"
admin.site.site_title = "Tra cứu hoá đơn 24/7"


class ReceiptAdmin(admin.ModelAdmin):
    search_fields = ["code", "description"]
    list_display = ["code", "description", "image", "created_at", "is_deleted"]
    list_filter = ["is_deleted", "created_at"]

    def has_add_permission(self, request):  # noqa: ARG002
        return False

    def has_change_permission(self, request, obj=None):  # noqa: ARG002
        return False

    def has_delete_permission(self, request, obj=None):  # noqa: ARG002
        return False


admin.site.register(Receipt, ReceiptAdmin)

admin.site.unregister(Group)
