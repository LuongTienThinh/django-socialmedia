# Generated by Django 4.2.6 on 2023-11-25 11:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0018_chatmessage_slug"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chatmessage",
            name="slug",
        ),
        migrations.AddField(
            model_name="chatmessage",
            name="chat_domain",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
