from django.test import TestCase
from django.urls import reverse


class TransfersViewTests(TestCase):
    def test_bulk_transfer_GET(self):
        response = self.client.get(reverse("bulk_transfer"))
        self.assertEqual(response.status_code, 405)

    def test_bulk_transfer_POST(self):
        response = self.client.post(reverse("bulk_transfer"))
        self.assertEqual(response.status_code, 200)
