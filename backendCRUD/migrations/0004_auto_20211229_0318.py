# Generated by Django 3.1.13 on 2021-12-29 03:18

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendCRUD', '0003_auto_20211229_0128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='valCompany',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=None), size=None),
        ),
    ]
