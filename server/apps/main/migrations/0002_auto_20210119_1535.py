# Generated by Django 2.2.17 on 2021-01-19 12:35

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="History",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="PassedPoll",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "answers",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=django.contrib.postgres.fields.ArrayField(
                            base_field=models.CharField(blank=True, max_length=100),
                            size=None,
                        ),
                        size=None,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Poll",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField()),
                ("description", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.TextField()),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("ONE", "One correct"),
                            ("MULTIPLE", "Multiple correct"),
                            ("TEXT", "Text answer"),
                        ],
                        max_length=100,
                    ),
                ),
                (
                    "variants",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(blank=True, max_length=100), size=10
                    ),
                ),
                (
                    "correct",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(blank=True, max_length=100), size=10
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="BlogPost",
        ),
        migrations.AddField(
            model_name="poll",
            name="questions",
            field=models.ManyToManyField(related_name="questions", to="main.Question"),
        ),
        migrations.AddField(
            model_name="passedpoll",
            name="poll",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="main.Poll"
            ),
        ),
        migrations.AddField(
            model_name="history",
            name="passes",
            field=models.ManyToManyField(to="main.PassedPoll"),
        ),
    ]
