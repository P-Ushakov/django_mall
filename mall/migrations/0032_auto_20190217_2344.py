# Generated by Django 2.1.5 on 2019-02-17 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mall', '0031_auto_20190217_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mlobjectindexpage',
            name='broken_if_num_elements_broken',
            field=models.IntegerField(default=0, verbose_name='группа сломана если N элементов требует ремонта'),
        ),
    ]
