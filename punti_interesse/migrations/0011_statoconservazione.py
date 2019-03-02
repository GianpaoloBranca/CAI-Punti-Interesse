# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-03-02 09:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('punti_interesse', '0010_puntointeresse_rilevatore'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatoConservazione',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descrizione', models.CharField(max_length=128, unique=True, verbose_name='Descrizione')),
            ],
            options={
                'verbose_name': 'Stato di Conservazione',
                'verbose_name_plural': 'Stati di Conservazione',
            },
        ),
    ]
