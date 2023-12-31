# Generated by Django 4.2.6 on 2023-11-07 14:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("social", "0012_remove_groupmembership_message"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="groupmembership",
            unique_together={("user", "group")},
        ),
        migrations.CreateModel(
            name="MembershipRequest",
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
                    "status",
                    models.CharField(
                        choices=[
                            ("requested", "Requested"),
                            ("approved", "Approved"),
                            ("rejected", "Rejected"),
                        ],
                        default="requested",
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="social.group"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
