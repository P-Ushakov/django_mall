# Generated by Django 2.1.5 on 2019-02-07 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mall', '0012_auto_20190207_1447'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mlobjectindexpage',
            old_name='subelements',
            new_name='sub_elements',
        ),
        migrations.RenameField(
            model_name='mlobjectpage',
            old_name='subelements',
            new_name='sub_elements',
        ),
    ]
