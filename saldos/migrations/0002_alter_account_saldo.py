# Generated by Django 4.1.2 on 2022-10-31 23:01

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saldos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='saldo',
            field=models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.00'), max_digits=10, null=True),
        ),
    ]
