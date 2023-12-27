# Generated by Django 4.2.6 on 2023-12-27 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0001_initial'),
        ('main', '0028_event_finish'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='club',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='club', to='club.club'),
        ),
    ]
