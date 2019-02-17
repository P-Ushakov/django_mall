# Generated by Django 2.1.5 on 2019-02-17 22:15

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mall', '0030_auto_20190211_1945'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mlobjectindexpage',
            name='broken_if_all_elements_broken',
        ),
        migrations.AddField(
            model_name='mlobjectindexpage',
            name='broken_if_num_elements_broken',
            field=models.BooleanField(default=0, verbose_name='группа сломана если N элементов требует ремонта'),
        ),
        migrations.AlterField(
            model_name='mlobjectautotag',
            name='content_object',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='ml_obj_auto_tags', to='mall.MlObjectPage'),
        ),
    ]
