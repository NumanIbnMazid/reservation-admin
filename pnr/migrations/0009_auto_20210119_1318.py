# Generated by Django 3.1.4 on 2021-01-19 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pnr', '0008_auto_20210119_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pnr',
            name='sabre_token',
            field=models.JSONField(blank=True, null=True, verbose_name='sabre token'),
        ),
    ]
