# Generated by Django 4.2.4 on 2024-01-20 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0012_luxury_room_luxuries'),
    ]

    operations = [
        migrations.AlterField(
            model_name='luxury',
            name='id',
            field=models.IntegerField(default=0, primary_key=True, serialize=False, unique=True),
        ),
    ]