from django.contrib import admin
from .models import APIToken

@admin.register(APIToken)
class APITokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at')
    readonly_fields = ('token', 'created_at')
    search_fields = ('user__username',)
