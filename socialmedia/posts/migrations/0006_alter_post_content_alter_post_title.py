# Generated by Django 4.2.6 on 2023-11-05 06:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0005_reply"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="content",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="post",
            name="title",
            field=models.TextField(blank=True),
        ),
    ]