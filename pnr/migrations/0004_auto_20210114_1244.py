# Generated by Django 3.1.4 on 2021-01-14 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pnr', '0003_pnr_data_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pnr',
            name='data_source',
            field=models.CharField(blank=True, choices=[('B2C', 'B2C'), ('B2B_AGENT', 'B2B_AGENT'), ('O', 'B2B_ADMIN')], max_length=20, null=True, verbose_name='data source'),
        ),
    ]
