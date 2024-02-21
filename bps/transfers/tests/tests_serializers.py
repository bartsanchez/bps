from django.test import TestCase
from django.urls import reverse


class SerializerTests(TestCase):
    def setUp(self):
        self.url = reverse("bulk_transfer")

    def test_bulk_transfer_one_credit_transfer(self):
        content = {
            "organization_name": "foo",
            "organization_iban": "bar",
            "organization_bic": "qux",
            "credit_transfers": [
                {
                    "amount": "14.5",
                    "counterparty_name": "Bip Bip",
                    "counterparty_bic": "CRLYFRPPTOU",
                    "counterparty_iban": "EE383680981021245685",
                    "description": "Wonderland/4410",
                },
            ],
        }
        response = self.client.post(
            self.url,
            data=content,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_bulk_transfer_more_than_one_credit_transfers(self):
        content = {
            "organization_name": "foo",
            "organization_iban": "bar",
            "organization_bic": "qux",
            "credit_transfers": [
                {
                    "amount": "14.5",
                    "counterparty_name": "Bip Bip",
                    "counterparty_bic": "CRLYFRPPTOU",
                    "counterparty_iban": "EE383680981021245685",
                    "description": "Wonderland/4410",
                },
                {
                    "amount": "61238",
                    "counterparty_name": "Wile E Coyote",
                    "counterparty_bic": "ZDRPLBQI",
                    "counterparty_iban": "DE9935420810036209081725212",
                    "description": "//TeslaMotors/Invoice/12",
                },
                {
                    "amount": "999",
                    "counterparty_name": "Bugs Bunny",
                    "counterparty_bic": "RNJZNTMC",
                    "counterparty_iban": "FR0010009380540930414023042",
                    "description": "2020 09 24/2020 09 25/GoldenCarrot/",
                },
            ],
        }
        response = self.client.post(
            self.url,
            data=content,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
