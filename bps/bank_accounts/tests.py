from django.test import TestCase

from .models import BankAccount


class BankAccountModelTests(TestCase):
    def setUp(self):
        self.bank_account = BankAccount.objects.create(
            organization_name="fake_organization",
            balance_cents=777,
            iban="FR10474608000002006107XXXXX",
            bic="OIVUSCLQXXX",
        )

    def test_str(self):
        self.assertEqual(str(self.bank_account), "BankAccount(id=1)")
