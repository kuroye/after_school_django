# Generated by Django 4.2.6 on 2023-10-26 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_character_max_item_alter_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='characteritem',
            name='item',
            field=models.ManyToManyField(blank=True, null=True, to='main.item'),
        ),
    ]
