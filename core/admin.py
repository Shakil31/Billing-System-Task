from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'model_name', 'user', 'timestamp')
    list_filter = ('action', 'model_name')
    readonly_fields = ('timestamp', 'details')
