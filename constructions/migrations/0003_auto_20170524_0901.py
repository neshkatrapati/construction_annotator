# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-24 09:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructions', '0002_auto_20170524_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='construction',
            name='participants',
            field=models.ManyToManyField(blank=True, to='constructions.ConstructionParticipant'),
        ),
    ]
