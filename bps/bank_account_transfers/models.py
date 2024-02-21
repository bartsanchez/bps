from django.db import models


class BankAccountTransfersRequest(models.Model):
    organization_name = models.TextField()
    organization_iban = models.TextField()
    organization_bic = models.TextField()

    def __str__(self):
        return f"BankAccountTransfersRequest(id={self.id})"
