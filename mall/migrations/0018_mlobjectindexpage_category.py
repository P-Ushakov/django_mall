# Generated by Django 2.1.5 on 2019-02-07 23:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mall', '0017_auto_20190207_2241'),
    ]

    operations = [
        migrations.AddField(
            model_name='mlobjectindexpage',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mall.MlCategory'),
        ),
    ]