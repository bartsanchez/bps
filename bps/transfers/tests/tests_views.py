import logging
from unittest import mock

from bank_accounts.models import BankAccount
from django.test import TestCase
from django.urls import reverse


class TransfersViewTests(TestCase):
    def setUp(self):
        self.url = reverse("bulk_transfer")
        bank_account = BankAccount(
            organization_name="a",
            iban="b",
            bic="c",
            balance_cents=0,
        )
        bank_account.save()

    def test_bulk_transfer_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_bulk_transfer_POST(self):
        response = self.client.post(
            self.url,
            data={
                "organization_name": "a",
                "organization_iban": "b",
                "organization_bic": "c",
                "credit_transfers": [],
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_bulk_transfer_POST_logged(self):
        logger = logging.getLogger("transfers.views")

        msg = {"foo": 1, "bar": 2, "spam": 3}

        with mock.patch.object(logger, "info") as log_mock:
            self.client.post(self.url, data=msg, content_type="application/json")
            log_mock.assert_called_once_with(
                "Received content: %(content)",
                extra={"content": '{"foo": 1, "bar": 2, "spam": 3}'},
            )


class IdempotencyTests(TestCase):
    def setUp(self):
        self.url = reverse("bulk_transfer")
        bank_account = BankAccount(
            organization_name="foo",
            iban="bar",
            bic="qux",
            balance_cents=0,
        )
        bank_account.save()
        self.content = {
            "organization_name": "foo",
            "organization_iban": "bar",
            "organization_bic": "qux",
            "credit_transfers": [],
        }

    def test_bulk_transfer_first_is_ok(self):
        response = self.client.post(
            self.url,
            data=self.content,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_bulk_transfer_second_is_not_allowed(self):
        response = self.client.post(
            self.url,
            data=self.content,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.url,
            data=self.content,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 422)
