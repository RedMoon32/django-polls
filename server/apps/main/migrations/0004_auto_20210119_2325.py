# Generated by Django 2.2.17 on 2021-01-19 20:25

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_auto_20210119_1918"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="answers",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=django.contrib.postgres.fields.ArrayField(
                    base_field=models.CharField(blank=True, max_length=100), size=10
                ),
                size=None,
            ),
        ),
    ]
