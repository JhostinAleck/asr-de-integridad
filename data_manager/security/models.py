from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.CharField(max_length=255)
    blocked_at = models.DateTimeField(default=timezone.now)
    block_expires = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.ip_address} (blocked at {self.blocked_at})"