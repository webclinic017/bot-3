# Generated by Django 2.2.24 on 2021-08-15 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trader', '0023_auto_20210815_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='closed',
            field=models.IntegerField(null=True, verbose_name='Закрыт'),
        ),
        migrations.AlterField(
            model_name='position',
            name='opened',
            field=models.IntegerField(verbose_name='Открыт'),
        ),
    ]
