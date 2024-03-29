# Generated by Django 3.2 on 2023-10-09 12:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingMedical',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=16)),
                ('description', models.TextField()),
                ('is_valid', models.BooleanField(default=False, verbose_name='is valid')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('village', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_village', to='accounts.village')),
                ('worker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='umujyanama_booked', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Booking Medical',
                'verbose_name_plural': 'Booking Medicals',
                'ordering': ('-created_on',),
            },
        ),
    ]
