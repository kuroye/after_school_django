# Generated by Django 4.2.6 on 2023-12-22 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_rename_hp_character_current_hp_character_max_hp'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='p2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='p2', to='main.character'),
        ),
    ]
