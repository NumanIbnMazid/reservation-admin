# Generated by Django 3.1.4 on 2021-01-19 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pnr', '0013_auto_20210119_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pnr',
            name='sabre_token',
            field=models.JSONField(verbose_name='sabre token'),
        ),
    ]
