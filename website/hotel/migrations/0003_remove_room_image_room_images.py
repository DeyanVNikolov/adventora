# Generated by Django 4.2.4 on 2023-11-17 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0002_delete_luxuryoption'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='image',
        ),
        migrations.AddField(
            model_name='room',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='room_images/'),
        ),
    ]
