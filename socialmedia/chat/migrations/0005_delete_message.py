# Generated by Django 4.2.6 on 2023-11-19 03:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0004_chatroom_message"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Message",
        ),
    ]