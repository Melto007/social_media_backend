# Generated by Django 3.2 on 2024-03-19 03:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follower',
            name='user',
        ),
        migrations.AlterField(
            model_name='tokenuser',
            name='expired_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 26, 3, 8, 17, 47285)),
        ),
    ]