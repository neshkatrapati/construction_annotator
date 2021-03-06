# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-02 04:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('constructions', '0003_auto_20170524_0901'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorpusFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2000)),
                ('uploaded_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='construction',
            name='participants',
            field=models.ManyToManyField(blank=True, null=True, to='constructions.ConstructionParticipant'),
        ),
        migrations.AddField(
            model_name='sentence',
            name='corpus_file',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='constructions.CorpusFile'),
            preserve_default=False,
        ),
    ]
