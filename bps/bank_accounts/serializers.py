from adrf.serializers import ModelSerializer
from rest_framework import serializers

from .models import BankAccount


class BankAccountSerializer(ModelSerializer):
    organization_iban = serializers.CharField(source="iban")
    organization_bic = serializers.CharField(source="bic")

    class Meta:
        model = BankAccount
        fields = ["organization_name", "organization_iban", "organization_bic"]
