from django.db import models
import hashlib


class ProcessedBulkTransfer(models.Model):
    request_hash = models.CharField(max_length=64)
    content = models.TextField()

    def __str__(self):
        return self.request_hash

    def save(self, *args, **kwargs):
        content = bytes(self.content, "utf-8")
        self.request_hash = hashlib.sha256(content).hexdigest()
        super().save(*args, **kwargs)
