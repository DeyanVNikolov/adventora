# Generated by Django 4.2.4 on 2024-01-22 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0017_alter_luxury_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='short_code',
            field=models.CharField(blank=True, default='<functio', max_length=100, null=True),
        ),
    ]
