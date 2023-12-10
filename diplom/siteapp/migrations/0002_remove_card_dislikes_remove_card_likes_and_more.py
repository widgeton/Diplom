# Generated by Django 5.0 on 2023-12-09 12:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("siteapp", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="card",
            name="dislikes",
        ),
        migrations.RemoveField(
            model_name="card",
            name="likes",
        ),
        migrations.AlterField(
            model_name="card",
            name="example",
            field=models.TextField(null=True),
        ),
        migrations.CreateModel(
            name="Like",
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
                (
                    "card",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="siteapp.card"
                    ),
                ),
                ("users", models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name="Mark",
        ),
    ]
