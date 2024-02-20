import hashlib

from django.test import TestCase

from transfers.models import ProcessedBulkTransfer


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
