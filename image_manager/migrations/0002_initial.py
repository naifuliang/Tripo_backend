# Generated by Django 4.2.5 on 2023-10-29 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('image_manager', '0001_initial'),
        ('tripo_main_interface', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image_item',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='tripo_main_interface.posts'),
        ),
    ]
