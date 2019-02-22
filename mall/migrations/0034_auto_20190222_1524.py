# Generated by Django 2.1.5 on 2019-02-22 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mall', '0033_mlobjectindexpage_is_visible_for_tags'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mlobjectindexpage',
            options={'verbose_name': 'список объектов', 'verbose_name_plural': 'списоки объектов'},
        ),
        migrations.RemoveField(
            model_name='mlobjectindexpage',
            name='broken_if_num_elements_broken',
        ),
        migrations.AddField(
            model_name='mlobjectindexpage',
            name='have_to_be_diagnosed',
            field=models.IntegerField(default=0, verbose_name='требует осмотра'),
        ),
        migrations.AddField(
            model_name='mlobjectindexpage',
            name='is_disabled',
            field=models.IntegerField(default=0, verbose_name='выключено'),
        ),
        migrations.AddField(
            model_name='mlobjectindexpage',
            name='need_service',
            field=models.IntegerField(default=0, verbose_name='требует ТО'),
        ),
        migrations.AddField(
            model_name='mlobjectindexpage',
            name='status_bad',
            field=models.IntegerField(default=0, verbose_name='статус Bad'),
        ),
        migrations.AddField(
            model_name='mlobjectindexpage',
            name='status_ok',
            field=models.IntegerField(default=0, verbose_name='статус OK'),
        ),
        migrations.AlterField(
            model_name='mlobjectindexpage',
            name='call_down',
            field=models.IntegerField(default=0, verbose_name='есть замечания'),
        ),
        migrations.AlterField(
            model_name='mlobjectindexpage',
            name='diagnosed',
            field=models.IntegerField(default=0, verbose_name='произведен осмотр'),
        ),
        migrations.AlterField(
            model_name='mlobjectindexpage',
            name='have_maintenance',
            field=models.IntegerField(default=0, verbose_name='пройдено ТО'),
        ),
        migrations.AlterField(
            model_name='mlobjectindexpage',
            name='have_to_be_repaired',
            field=models.IntegerField(default=0, verbose_name='требует ремонта'),
        ),
        migrations.AlterField(
            model_name='mlobjectindexpage',
            name='is_critical',
            field=models.IntegerField(default=0, verbose_name='группа критически важна'),
        ),
        migrations.AlterField(
            model_name='mlobjectindexpage',
            name='is_critically_broken',
            field=models.IntegerField(default=0, verbose_name='группа сломана'),
        ),
        migrations.AlterField(
            model_name='mlobjectindexpage',
            name='is_enabled',
            field=models.IntegerField(default=0, verbose_name='включено'),
        ),
        migrations.AlterField(
            model_name='mlobjectpage',
            name='is_critically_broken',
            field=models.BooleanField(default=False, verbose_name='сломан'),
        ),
    ]
