from django.test import TestCase

from .serializers import BankAccountTransfersRequestSerializer


class SerializerTests(TestCase):
    def test_requested_amount(self):
        data = {
            "organization_name": "foo",
            "organization_iban": "bar",
            "organization_bic": "qux",
            "credit_transfers": [
                {
                    "amount": "14.5",
                    "counterparty_name": "a",
                    "counterparty_bic": "b",
                    "counterparty_iban": "c",
                    "description": "d",
                },
                {
                    "amount": "666.6",
                    "counterparty_name": "e",
                    "counterparty_bic": "f",
                    "counterparty_iban": "g",
                    "description": "h",
                },
            ],
        }
        serializer = BankAccountTransfersRequestSerializer(data=data)
        self.assertTrue(serializer.is_valid())
