import secrets
from django.db import models
from django.contrib.auth.models import User

class APIToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='api_token')
    token = models.CharField(max_length=64, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_hex(32)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Token for {self.user.username}"


class APIRequestLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='api_logs')
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    request_data = models.TextField(blank=True)
    response_status = models.IntegerField()
    response_time = models.FloatField(help_text="Response time in milliseconds")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.method} {self.endpoint} - {self.response_status} ({self.timestamp})"
