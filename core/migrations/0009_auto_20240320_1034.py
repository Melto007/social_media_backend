# Generated by Django 3.2 on 2024-03-20 05:04

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20240320_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='tag', to='core.tag'),
        ),
        migrations.AlterField(
            model_name='tokenuser',
            name='expired_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 27, 5, 4, 48, 107152)),
        ),
    ]
