# Generated by Django 3.1.4 on 2021-03-10 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0003_auto_20210303_1839'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationsetting',
            name='skytrip_address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='skytrip address'),
        ),
    ]
