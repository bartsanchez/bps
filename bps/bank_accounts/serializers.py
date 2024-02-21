from adrf.serializers import ModelSerializer
from rest_framework import serializers
from transfers.serializers import TransferSerializer

from .models import BankAccount


class BankAccountSerializer(ModelSerializer):
    organization_iban = serializers.CharField(source="iban")
    organization_bic = serializers.CharField(source="bic")
    credit_transfers = TransferSerializer(many=True, source="transfers")

    class Meta:
        model = BankAccount
        fields = [
            "organization_name",
            "organization_iban",
            "organization_bic",
            "credit_transfers",
        ]
