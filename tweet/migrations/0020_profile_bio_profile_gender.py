# Generated by Django 5.0.7 on 2025-01-18 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0019_rename_number_comment_tweet_save_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
