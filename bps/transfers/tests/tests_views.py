import json
import logging
from unittest import mock

from django.test import TestCase
from django.urls import reverse


class TransfersViewTests(TestCase):
    def setUp(self):
        self.url = reverse("bulk_transfer")

    def test_bulk_transfer_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_bulk_transfer_POST(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)

    def test_bulk_transfer_POST_logged(self):
        logger = logging.getLogger("transfers.views")

        msg = "{foo=1, bar=2, spam=3}"

        with mock.patch.object(logger, "info") as log_mock:
            self.client.post(self.url, data=msg, content_type="application/json")
            log_mock.assert_called_once_with(
                "Received content: %(content)",
                extra={"content": msg},
            )


class IdempotencyTests(TestCase):
    def setUp(self):
        self.url = reverse("bulk_transfer")
        self.content = '{"foo": 1, "bar": 2}'
        self.content_json = json.loads(self.content)

    def test_bulk_transfer_first_is_ok(self):
        response = self.client.post(
            self.url,
            data=self.content_json,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_bulk_transfer_second_is_not_allowed(self):
        response = self.client.post(
            self.url,
            data=self.content_json,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.url,
            data=self.content_json,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 422)