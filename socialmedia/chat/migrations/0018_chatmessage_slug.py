# Generated by Django 4.2.6 on 2023-11-25 10:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0017_chatmessage_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="chatmessage",
            name="slug",
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
