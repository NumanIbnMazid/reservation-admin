# Generated by Django 3.1.4 on 2021-02-11 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pnr', '0024_auto_20210211_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pnrcarriercodestats',
            name='pnr_list',
            field=models.JSONField(blank=True, default=dict, null=True, verbose_name='pnr list'),
        ),
    ]