import decimal

from adrf.serializers import ModelSerializer
from rest_framework import serializers

from .models import Transfer


class TransferSerializer(ModelSerializer):
    amount = serializers.CharField(source="amount_cents")

    class Meta:
        model = Transfer
        fields = [
            "amount",
            "counterparty_name",
            "counterparty_bic",
            "counterparty_iban",
            "description",
        ]

    def validate_amount(self, value):
        try:
            amount = decimal.Decimal(value)
        except decimal.InvalidOperation as exc:
            raise serializers.ValidationError("Incorrect amount") from exc

        if amount <= decimal.Decimal("0"):
            raise serializers.ValidationError("Incorrect amount")

        return value
