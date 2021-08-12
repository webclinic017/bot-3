# Generated by Django 2.2.24 on 2021-08-12 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trader', '0008_auto_20210812_1145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trades',
            name='balance_eth',
        ),
        migrations.RemoveField(
            model_name='trades',
            name='balance_usd',
        ),
        migrations.AddField(
            model_name='position',
            name='strike',
            field=models.FloatField(blank=True, null=True, verbose_name='Страйк'),
        ),
        migrations.AlterField(
            model_name='position',
            name='sell_price',
            field=models.FloatField(blank=True, null=True, verbose_name='Продажа'),
        ),
    ]
