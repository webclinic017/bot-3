# Generated by Django 2.2.24 on 2021-08-12 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trader', '0007_auto_20210811_1942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='strategy',
            name='balance_eth',
        ),
        migrations.AlterField(
            model_name='strategy',
            name='balance_usd',
            field=models.FloatField(verbose_name='стартовый USD'),
        ),
    ]
