# Generated by Django 4.2.6 on 2023-11-21 14:25

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0009_alter_message_options_chatmessage"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Message",
        ),
    ]
