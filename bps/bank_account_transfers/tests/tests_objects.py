from bank_accounts.models import BankAccount
from django.test import TestCase
from django.urls import reverse
from transfers.models import Transfer

from bank_account_transfers.models import BankAccountTransfersRequest


class ObjectsCreationTests(TestCase):
    def setUp(self):
        self.url = reverse("bulk_transfer")
        bank_account = BankAccount(
            organization_name="a",
            iban="b",
            bic="c",
            balance_cents=1800,
        )
        bank_account.save()

    def test_bulk_transfer_objects_created(self):
        self.assertEqual(BankAccountTransfersRequest.objects.count(), 0)
        self.assertEqual(Transfer.objects.count(), 0)
        self.assertEqual(BankAccount.objects.filter(iban="b").count(), 1)

        bank_account = BankAccount.objects.get(iban="b")
        self.assertEqual(bank_account.balance_cents, 1800)

        response = self.client.post(
            self.url,
            data={
                "organization_name": "a",
                "organization_iban": "b",
                "organization_bic": "c",
                "credit_transfers": [
                    {
                        "amount": "7.1",
                        "counterparty_name": "d",
                        "counterparty_bic": "e",
                        "counterparty_iban": "f",
                        "description": "g",
                    },
                    {
                        "amount": "10.4",
                        "counterparty_name": "h",
                        "counterparty_bic": "i",
                        "counterparty_iban": "j",
                        "description": "k",
                    },
                ],
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(BankAccountTransfersRequest.objects.count(), 1)

        bank_account_transfer_request = BankAccountTransfersRequest.objects.first()
        self.assertEqual(bank_account_transfer_request.organization_iban, "b")

        self.assertEqual(Transfer.objects.count(), 2)

        first_transfer = Transfer.objects.get(counterparty_iban="f")
        self.assertEqual(first_transfer.counterparty_name, "d")
        self.assertEqual(first_transfer.counterparty_bic, "e")
        self.assertEqual(first_transfer.description, "g")
        self.assertEqual(first_transfer.amount_cents, 710)

        second_transfer = Transfer.objects.get(counterparty_iban="j")
        self.assertEqual(second_transfer.counterparty_name, "h")
        self.assertEqual(second_transfer.counterparty_bic, "i")
        self.assertEqual(second_transfer.description, "k")
        self.assertEqual(second_transfer.amount_cents, 1040)

        bank_account = BankAccount.objects.get(iban="b")
        self.assertEqual(bank_account.balance_cents, 50)
