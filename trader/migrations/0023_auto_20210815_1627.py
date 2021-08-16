# Generated by Django 2.2.24 on 2021-08-15 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trader', '0022_auto_20210815_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variants',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Сумма сделки'),
        ),
        migrations.AlterField(
            model_name='variants',
            name='balance_usd',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='стартовый USD'),
        ),
        migrations.AlterField(
            model_name='variants',
            name='profit_percent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Процент прибыли'),
        ),
        migrations.AlterField(
            model_name='variants',
            name='step',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Шаг позиции'),
        ),
    ]
