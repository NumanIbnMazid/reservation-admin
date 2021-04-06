# Generated by Django 3.1.4 on 2021-01-28 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_auto_20210128_1554'),
        ('pnr', '0019_auto_20210128_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pnr',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_pnr', to='payment.payment', verbose_name='payment'),
        ),
    ]