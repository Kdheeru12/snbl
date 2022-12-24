# Generated by Django 2.2.25 on 2022-12-24 14:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tortoise", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plan",
            name="benefitPercentage",
            field=models.FloatField(
                default=0, validators=[django.core.validators.MaxValueValidator(100.0)]
            ),
        ),
        migrations.AlterField(
            model_name="promotion",
            name="benefitPercentage",
            field=models.FloatField(
                default=0, validators=[django.core.validators.MaxValueValidator(100.0)]
            ),
        ),
    ]
