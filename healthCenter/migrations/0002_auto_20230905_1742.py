# Generated by Django 3.2 on 2023-09-05 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthCenter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='birthchild',
            name='is_valid',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
        migrations.AddField(
            model_name='pregnancy',
            name='is_valid',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
    ]