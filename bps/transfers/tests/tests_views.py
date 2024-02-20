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
