from django.contrib import admin
from django.contrib.auth.models import Group

from app.models import Receipt

admin.site.site_header = "Tra cứu hoá đơn 24/7"
admin.site.site_title = "Tra cứu hoá đơn 24/7"


class ReceiptAdmin(admin.ModelAdmin):
    search_fields = ["code", "description"]
    list_display = ["code", "description", "image", "created_at"]


admin.site.register(Receipt, ReceiptAdmin)

admin.site.unregister(Group)
