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
