# Generated by Django 2.1.5 on 2019-02-09 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('mall', '0023_mlobjdisposer'),
    ]

    operations = [
        migrations.AddField(
            model_name='mlobjectpage',
            name='disposer_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page'),
        ),
    ]
