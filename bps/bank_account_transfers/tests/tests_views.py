import logging
from unittest import mock

import django
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
        self.assertEqual(response.status_code, 201)

    def test_bulk_transfer_POST_logged(self):
        logger = logging.getLogger("bank_account_transfers.views")

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
        self.assertEqual(response.status_code, 201)

    def test_bulk_transfer_second_is_not_allowed(self):
        response = self.client.post(
            self.url,
            data=self.content,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

        response = self.client.post(
            self.url,
            data=self.content,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 422)


class SomethingBreaksTests(TestCase):
    def setUp(self):
        self.url = reverse("bulk_transfer")
        bank_account = BankAccount(
            organization_name="AA",
            iban="BB",
            bic="CC",
            balance_cents=1000,
        )
        bank_account.save()
        self.content = {
            "organization_name": "AA",
            "organization_iban": "BB",
            "organization_bic": "CC",
            "credit_transfers": [
                {
                    "amount": "1",
                    "counterparty_name": "DD",
                    "counterparty_bic": "EE",
                    "counterparty_iban": "FF",
                    "description": "GG",
                },
            ],
        }

    @mock.patch("bank_account_transfers.views.mark_as_processed")
    def test_orm_is_broken(self, orm_mock):
        def _orm_exception_side_effect(_):
            raise django.db.utils.OperationalError

        orm_mock.side_effect = _orm_exception_side_effect

        with self.assertRaises(django.db.utils.OperationalError):
            self.client.post(
                self.url,
                data=self.content,
                content_type="application/json",
            )

        orm_mock.assert_called_once()
