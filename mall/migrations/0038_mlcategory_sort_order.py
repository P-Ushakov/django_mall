# Generated by Django 2.1.5 on 2019-02-24 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mall', '0037_auto_20190224_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='mlcategory',
            name='sort_order',
            field=models.IntegerField(blank=True, editable=False, null=True),
        ),
    ]
