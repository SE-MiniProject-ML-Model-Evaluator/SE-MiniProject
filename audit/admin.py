from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "user_email", "action", "detail", "ip_address")
    list_filter = ("action",)
    search_fields = ("user_email", "detail")
