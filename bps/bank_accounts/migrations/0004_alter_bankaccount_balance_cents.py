# Generated by Django 5.0.2 on 2024-02-21 16:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bank_accounts", "0003_alter_bankaccount_balance_cents"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bankaccount",
            name="balance_cents",
            field=models.PositiveBigIntegerField(),
        ),
    ]
