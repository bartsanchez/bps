from decimal import Decimal

from adrf.serializers import ModelSerializer
from bank_accounts.models import BankAccount
from rest_framework import serializers
from transfers.models import Transfer
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

    def create(self, validated_data):
        transfers_data = validated_data.pop("transfers")
        bank_account_transfers_request = BankAccountTransfersRequest.objects.create(
            **validated_data,
        )
        bank_account = BankAccount.objects.get(
            iban=bank_account_transfers_request.organization_iban,
        )
        for transfer_data in transfers_data:
            transfer = Transfer(
                bank_account=bank_account,
                bank_account_transfers_request=bank_account_transfers_request,
                **transfer_data,
            )
            transfer.save()
        return bank_account_transfers_request

    def requested_amount(self):
        return sum(
            [Decimal(ct["amount_cents"]) for ct in self.validated_data["transfers"]],
        ) or Decimal("0")

    def requested_amount_cents(self):
        return (self.requested_amount() * 100).to_integral_exact()
