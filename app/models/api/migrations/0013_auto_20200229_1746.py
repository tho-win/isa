# Generated by Django 2.2.4 on 2020-02-29 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20200229_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='price',
            field=models.FloatField(),
        ),
    ]
