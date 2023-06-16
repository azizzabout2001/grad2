# Generated by Django 4.2.2 on 2023-06-16 16:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_users', '0004_remove_provider_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='rating',
            field=models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)]),
        ),
    ]