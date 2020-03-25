# Generated by Django 2.2.4 on 2020-03-22 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DummyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(default='', max_length=254, unique=True)),
                ('username', models.CharField(max_length=30)),
                ('first_name', models.CharField(blank=True, max_length=20)),
                ('last_name', models.CharField(blank=True, max_length=20)),
                ('computing_id', models.CharField(default='', max_length=10)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('bio', models.TextField(blank=True, max_length=500)),
            ],
        ),
    ]
