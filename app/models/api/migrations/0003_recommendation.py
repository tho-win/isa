# Generated by Django 2.2.4 on 2020-05-04 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200325_1651'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('co_views', models.CharField(default='', max_length=3000)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Post')),
            ],
        ),
    ]