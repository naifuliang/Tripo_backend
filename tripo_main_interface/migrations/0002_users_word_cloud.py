# Generated by Django 4.2.5 on 2023-11-03 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tripo_main_interface', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='word_cloud',
            field=models.ImageField(default='../media/static/default_avatar.jpg', upload_to='word_clouds'),
        ),
    ]
