# Generated by Django 4.2.6 on 2023-12-23 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_event_victory'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='audio',
            field=models.FileField(blank=True, null=True, upload_to='audio/skill/'),
        ),
    ]
