# Generated by Django 2.2.4 on 2020-02-28 21:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20200228_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]