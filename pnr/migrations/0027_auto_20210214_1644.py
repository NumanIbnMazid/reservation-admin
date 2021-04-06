# Generated by Django 3.1.4 on 2021-02-14 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pnr', '0026_auto_20210211_1942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pnr',
            name='user',
        ),
        migrations.AddField(
            model_name='pnr',
            name='user_id',
            field=models.CharField(default=1, max_length=100, verbose_name='user id'),
            preserve_default=False,
        ),
    ]