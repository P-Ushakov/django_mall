# Generated by Django 2.1.5 on 2019-02-06 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mall', '0005_auto_20190205_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mlobjectpage',
            name='intro',
            field=models.TextField(blank=True, verbose_name='краткое описание'),
        ),
    ]