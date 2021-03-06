# Generated by Django 3.1.4 on 2021-01-14 12:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0009_auto_20210114_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_created_by', to=settings.AUTH_USER_MODEL, verbose_name='created by'),
        ),
    ]
