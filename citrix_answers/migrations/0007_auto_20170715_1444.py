# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-15 09:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citrix_answers', '0006_question_has_solution'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='tag_name',
            new_name='name',
        ),
    ]
