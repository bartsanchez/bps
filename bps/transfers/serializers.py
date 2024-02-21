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
