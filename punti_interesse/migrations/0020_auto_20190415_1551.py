# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-04-15 13:51
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import punti_interesse.validators


class Migration(migrations.Migration):

    dependencies = [
        ('punti_interesse', '0019_userinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='GruppoMontuoso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Gruppo Montuoso',
                'verbose_name_plural': 'Gruppi Montuosi',
            },
        ),
        migrations.AlterField(
            model_name='puntointeresse',
            name='descr_breve',
            field=models.TextField(max_length=256, verbose_name='Descrizione oggetto breve*'),
        ),
        migrations.AlterField(
            model_name='puntointeresse',
            name='descr_estesa',
            field=models.TextField(max_length=1024, verbose_name='Descrizione oggetto estesa*'),
        ),
        migrations.AlterField(
            model_name='puntointeresse',
            name='descr_sito',
            field=models.TextField(max_length=256, verbose_name='Descrizione sito*'),
        ),
        migrations.AlterField(
            model_name='puntointeresse',
            name='foto_copertina',
            field=models.ImageField(default='', upload_to='foto_copertina/', validators=[punti_interesse.validators.MaxSizeValidator(2)], verbose_name='Foto copertina*'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='puntointeresse',
            name='istituto',
            field=models.CharField(blank=True, max_length=50, verbose_name='Istituto di tutela'),
        ),
        migrations.AlterField(
            model_name='puntointeresse',
            name='localita',
            field=models.CharField(max_length=75, verbose_name='Località*'),
        ),
        migrations.AlterField(
            model_name='puntointeresse',
            name='nome',
            field=models.CharField(max_length=50, verbose_name='Nome*'),
        ),
        migrations.AlterField(
            model_name='puntointeresse',
            name='periodo',
            field=models.CharField(blank=True, max_length=50, verbose_name='Periodo di visita consigliato'),
        ),
        migrations.AlterField(
            model_name='puntointeresse',
            name='valenza',
            field=models.CharField(max_length=30, verbose_name='Titolo della valenza*'),
        ),
        migrations.AlterField(
            model_name='puntointeresse',
            name='valle',
            field=models.CharField(blank=True, max_length=75, verbose_name='Valle'),
        ),
        migrations.AlterField(
            model_name='validazionepunto',
            name='comunita_montana',
            field=models.CharField(blank=True, max_length=128, verbose_name='Comunità montana'),
        ),
        migrations.AlterField(
            model_name='validazionepunto',
            name='descrizione',
            field=models.TextField(max_length=256, verbose_name='Descrizione*'),
        ),
        migrations.AlterField(
            model_name='validazionepunto',
            name='gruppo_montuoso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='punti_interesse.GruppoMontuoso', verbose_name='Gruppo Montuoso'),
        ),
        migrations.AlterField(
            model_name='validazionepunto',
            name='quota',
            field=models.DecimalField(decimal_places=0, max_digits=4, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Quota*'),
        ),
        migrations.AlterField(
            model_name='validazionepunto',
            name='regione',
            field=models.CharField(choices=[('VDA', "Valle d'Aosta"), ('PIE', 'Piemonte'), ('LOM', 'Lombardia'), ('TAA', 'Trentino Alto Adige'), ('VEN', 'Veneto'), ('FVG', 'Friuli Venezia Giulia'), ('LIG', 'Liguria'), ('ERM', 'Emilia Romagna'), ('TOS', 'Toscana'), ('UMB', 'Umbria'), ('MAR', 'Marche'), ('LAZ', 'Lazio'), ('ABR', 'Abruzzo'), ('MOL', 'Molise'), ('CAM', 'Campania'), ('BAS', 'Basilicata'), ('PUG', 'Puglia'), ('CAL', 'Calabria'), ('SIC', 'Sicilia'), ('SAR', 'Sardegna')], max_length=30, verbose_name='Regione*'),
        ),
    ]
