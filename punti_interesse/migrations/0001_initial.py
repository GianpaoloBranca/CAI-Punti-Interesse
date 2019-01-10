# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-10 14:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TipoInteresse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descrizione', models.CharField(max_length=128, unique=True)),
            ],
            options={
                'verbose_name': 'Tipo di Interesse',
                'verbose_name_plural': 'Tipi di Interesse',
            },
        ),
    ]
