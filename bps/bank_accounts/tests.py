from django.test import TestCase

from .models import BankAccount


class BankAccountModelTests(TestCase):
    def setUp(self):
        self.bank_account = BankAccount.objects.create(
            organization_name="fake_organization",
            balance_cents=777,
            iban="fake_iban",
            bic="fake_bic",
        )

    def test_str(self):
        self.assertEqual(
            str(self.bank_account),
            f"BankAccount(id={self.bank_account.id})",
        )
