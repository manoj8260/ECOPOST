# Generated by Django 5.0.7 on 2025-01-18 15:31

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0023_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='uploaded_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
