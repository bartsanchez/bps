import hashlib
from decimal import Decimal

from bank_accounts.models import BankAccount
from django.db import models


class ProcessedBulkTransfer(models.Model):
    request_hash = models.CharField(max_length=64)
    content = models.TextField()

    def __str__(self):
        return self.request_hash

    def save(self, *args, **kwargs):
        content = bytes(self.content, "utf-8")
        self.request_hash = hashlib.sha256(content).hexdigest()
        super().save(*args, **kwargs)


class Transfer(models.Model):
    counterparty_name = models.TextField()
    counterparty_iban = models.TextField()
    counterparty_bic = models.TextField()
    amount_cents = models.IntegerField()
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"Transfer(id={self.id})"

    def save(self, *args, **kwargs):
        amount = Decimal(self.amount_cents)
        self.amount_cents = (amount * 100).to_integral_exact()
        super().save(*args, **kwargs)
