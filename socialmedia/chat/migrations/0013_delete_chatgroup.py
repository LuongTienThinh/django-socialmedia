# Generated by Django 4.2.6 on 2023-11-22 00:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0012_chatgroup_remove_roommessage_room_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="ChatGroup",
        ),
    ]
