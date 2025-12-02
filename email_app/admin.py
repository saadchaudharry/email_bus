from django.contrib import admin
from .models import APIToken, APIRequestLog

@admin.register(APIToken)
class APITokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at')
    readonly_fields = ('token', 'created_at')
    search_fields = ('user__username',)


@admin.register(APIRequestLog)
class APIRequestLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'method', 'endpoint', 'response_status', 'response_time', 'ip_address')
    list_filter = ('method', 'response_status', 'timestamp')
    search_fields = ('user__username', 'endpoint', 'ip_address')
    readonly_fields = ('timestamp', 'user', 'endpoint', 'method', 'request_data', 'response_status', 'response_time', 'ip_address')
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        return False  # Logs are created automatically

