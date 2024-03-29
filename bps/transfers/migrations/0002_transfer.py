# Generated by Django 5.0.2 on 2024-02-21 08:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bank_accounts", "0001_initial"),
        ("transfers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Transfer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("counterparty_name", models.TextField()),
                ("counterparty_iban", models.TextField()),
                ("counterparty_bic", models.TextField()),
                ("amount_cents", models.IntegerField()),
                ("description", models.TextField()),
                (
                    "bank_account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bank_accounts.bankaccount",
                    ),
                ),
            ],
        ),
    ]
