# Generated by Django 5.0.7 on 2025-01-06 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0007_tweet_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
