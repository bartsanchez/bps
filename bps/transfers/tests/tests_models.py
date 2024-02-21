import hashlib

from bank_accounts.models import BankAccount
from django.test import TestCase

from transfers.models import ProcessedBulkTransfer, Transfer


class ProcessedBulkTransferModelTests(TestCase):
    def setUp(self):
        self.processed_bulk_transfer = ProcessedBulkTransfer.objects.create(
            content="foo",
        )

    def test_str(self):
        self.assertEqual(
            str(self.processed_bulk_transfer),
            hashlib.sha256(b"foo").hexdigest(),
        )

    def test_request_hash_field_automatically_generated(self):
        self.assertEqual(
            self.processed_bulk_transfer.request_hash,
            hashlib.sha256(b"foo").hexdigest(),
        )

    def test_content(self):
        self.assertEqual(self.processed_bulk_transfer.content, "foo")


class TransferModelTests(TestCase):
    def setUp(self):
        bank_account = BankAccount.objects.create(
            organization_name="fake_organization",
            balance_cents=777,
            iban="invented_iban",
            bic="invented_bic",
        )
        self.transfer = Transfer.objects.create(
            counterparty_name="Bip Bip",
            counterparty_iban="EE383680981021245685",
            counterparty_bic="CRLYFRPPTOU",
            amount_cents="14.5",
            bank_account=bank_account,
            description="Wonderland/4410",
        )

    def test_str(self):
        self.assertEqual(str(self.transfer), f"Transfer(id={self.transfer.id})")


class TransferAmountCentsTests(TestCase):
    def setUp(self):
        self.bank_account = BankAccount.objects.create(
            organization_name="fake_organization",
            balance_cents=777,
            iban="another_iban",
            bic="another_bic",
        )

    def test_cents_calculated_correctly(self):
        transfer = Transfer.objects.create(
            counterparty_name="Bip Bip",
            counterparty_iban="EE383680981021245685",
            counterparty_bic="CRLYFRPPTOU",
            amount_cents="14.5",
            bank_account=self.bank_account,
            description="Wonderland/4410",
        )
        self.assertEqual(transfer.amount_cents, 1450)

    def test_cents_calculated_two_decimals(self):
        transfer = Transfer.objects.create(
            counterparty_name="Bip Bip",
            counterparty_iban="EE383680981021245685",
            counterparty_bic="CRLYFRPPTOU",
            amount_cents="14.57",
            bank_account=self.bank_account,
            description="Wonderland/4410",
        )
        self.assertEqual(transfer.amount_cents, 1457)

    def test_cents_calculated_no_decimals(self):
        transfer = Transfer.objects.create(
            counterparty_name="Bip Bip",
            counterparty_iban="EE383680981021245685",
            counterparty_bic="CRLYFRPPTOU",
            amount_cents="14",
            bank_account=self.bank_account,
            description="Wonderland/4410",
        )
        self.assertEqual(transfer.amount_cents, 1400)
