from django.db import models


class BankAccount(models.Model):
    organization_name = models.TextField()
    balance_cents = models.IntegerField()
    iban = models.TextField(unique=True)
    bic = models.TextField(unique=True)

    def __str__(self):
        return f"BankAccount(id={self.id})"
