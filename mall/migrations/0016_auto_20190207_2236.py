# Generated by Django 2.1.5 on 2019-02-07 22:36

from django.db import migrations


class Migration(migrations.Migration):

    atomic = False
    dependencies = [
        ('mall', '0015_auto_20190207_2043'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MlGroup',
            new_name='MlCategory',
        ),
        migrations.AlterModelOptions(
            name='mlcategory',
            options={'verbose_name': 'категория группы объектов', 'verbose_name_plural': 'категория группы объектов'},
        ),
        migrations.AlterModelOptions(
            name='mlobjecttagindexpage',
            options={'verbose_name': 'ключи поиска', 'verbose_name_plural': 'ключи поиска'},
        ),
    ]
