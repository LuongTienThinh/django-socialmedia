# Generated by Django 4.2.6 on 2023-11-23 15:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0015_rename_room_chatroom_rename_chatgroup_roommessage"),
    ]

    operations = [
        migrations.AddField(
            model_name="roommessage",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="messages/images/"
            ),
        ),
    ]