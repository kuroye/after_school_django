# Generated by Django 4.2.6 on 2023-12-28 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0001_initial'),
        ('main', '0030_choice_club'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='club',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='club_skill', to='club.club'),
        ),
    ]
