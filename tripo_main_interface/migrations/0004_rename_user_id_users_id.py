# Generated by Django 4.1 on 2023-09-17 04:36

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tripo_main_interface", "0003_auto_20230917_1235"),
    ]

    operations = [
        migrations.RenameField(
            model_name="users",
            old_name="user_id",
            new_name="id",
        ),
    ]
