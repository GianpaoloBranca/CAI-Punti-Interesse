# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-11 13:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('punti_interesse', '0004_auto_20190111_1312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='puntointeresse',
            name='coordinate',
        ),
        migrations.AddField(
            model_name='puntointeresse',
            name='latitudine',
            field=models.DecimalField(decimal_places=6, default=12, max_digits=9, verbose_name='Latitudine'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='puntointeresse',
            name='longitudine',
            field=models.DecimalField(decimal_places=6, default=12, max_digits=9, verbose_name='Longitudine'),
            preserve_default=False,
        ),
    ]
