# Generated by Django 2.2.3 on 2019-09-29 14:30

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filemanager', '0002_item_todolist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10), size=8), blank=True, null=True, size=8),
        ),
    ]
