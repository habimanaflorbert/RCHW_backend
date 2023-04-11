# Generated by Django 4.1.5 on 2023-02-17 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_district_province_sector_remove_user_district_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='identification_insurance_number',
        ),
        migrations.RemoveField(
            model_name='user',
            name='insurance_type',
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('ADMIN', 'Super User'), ('STAFF', 'Staff User'), ('UMUJYANAMA', 'Umujyana')], default='STAFF', max_length=50, verbose_name='user type'),
        ),
    ]