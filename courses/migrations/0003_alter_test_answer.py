# Generated by Django 3.2.4 on 2022-05-21 18:10

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='answer',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
    ]
