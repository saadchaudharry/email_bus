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
