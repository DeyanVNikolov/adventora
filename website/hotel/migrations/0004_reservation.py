# Generated by Django 4.2.4 on 2023-11-19 09:23

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0003_remove_room_image_room_images'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('reserved_by', models.CharField(blank=True, max_length=5000, null=True)),
                ('checkin', models.DateField(blank=True, null=True)),
                ('checkout', models.DateField(blank=True, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('hotel', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='hotel.hotel')),
                ('room', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='hotel.room')),
            ],
            options={
                'verbose_name': 'Reservation',
                'verbose_name_plural': 'Reservations',
            },
        ),
    ]
