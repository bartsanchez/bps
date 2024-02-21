from decimal import Decimal

from adrf.serializers import ModelSerializer
from rest_framework import serializers
from transfers.serializers import TransferSerializer

from .models import BankAccountTransfersRequest


class BankAccountTransfersRequestSerializer(ModelSerializer):
    organization_iban = serializers.CharField()
    organization_bic = serializers.CharField()
    credit_transfers = TransferSerializer(many=True, source="transfers")

    class Meta:
        model = BankAccountTransfersRequest
        fields = [
            "organization_name",
            "organization_iban",
            "organization_bic",
            "credit_transfers",
        ]

    def requested_amount(self):
        return sum([Decimal(ct["amount"]) for ct in self.validated_data["transfers"]])

    def requested_amount_cents(self):
        return (self.requested_amount() * 100).to_integral_exact()
