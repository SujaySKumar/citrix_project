# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-15 10:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citrix_answers', '0007_auto_20170715_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='rating',
            field=models.IntegerField(default=10),
        ),
    ]
