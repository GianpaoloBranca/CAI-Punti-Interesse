from django.db import models
from django.template.defaultfilters import slugify

class PuntoInteresse(models.Model):
    longitudine = models.DecimalField(verbose_name='Longitudine', max_digits=9, decimal_places=6)
    latitudine = models.DecimalField(verbose_name='Latitudine', max_digits=9, decimal_places=6)

    categoria = models.ForeignKey('TipoInteresse', verbose_name='Tipologia')
    tipo = models.ForeignKey('InteresseSpecifico', verbose_name='Oggetto Specifico')

    nome = models.CharField(verbose_name='Nome', max_length=128)
    localita = models.CharField(verbose_name='Località', max_length=128)
    valle = models.CharField(verbose_name='Valle', max_length=128)
    qualita = models.ForeignKey('QualitaInteresse', verbose_name='Qualità interesse')
    estensione = models.ForeignKey('EstensioneInteresse', verbose_name='Estensione Interesse')

    valenza = models.CharField(verbose_name='Titolo della valenza', max_length=128)
    visitabile = models.BooleanField(verbose_name='Visitabile')
    visitabile2 = models.BooleanField(verbose_name='Visitabile per persone con ridotta capacità motoria o sensoriale')
    periodo = models.CharField(verbose_name='Periodo di visita consigliato', max_length=256)
    istituto = models.CharField(verbose_name='Istituto di tutela', max_length=128)

    #foto copertina (max 1)
    #foto accessorie (max 5)

    descr_breve = models.TextField(verbose_name='Descrizione oggetto breve', max_length=256)
    descr_estesa = models.TextField(verbose_name='Descrizione oggetto estesa', max_length=1024)
    descr_sito = models.TextField(verbose_name='Descrizione oggetto breve', max_length=256)

    #stato di conservazione

    motivo = models.TextField(verbose_name='Motivo per la fruizione', max_length=256)

    #riferimenti bibiliografici
    #riferimenti sitografici
    #rilevatore (utente)

    data = models.DateField(verbose_name='Data inserimento', auto_now=True)

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nome)
        super(PuntoInteresse, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Punto di Interesse'
        verbose_name_plural = 'Punti di Interesse'

    def __str__(self):
        return self.nome


class ValidazionePunto(models.Model):
    punto = models.OneToOneField(PuntoInteresse, on_delete=models.CASCADE, primary_key=True)

    validatore = models.CharField(verbose_name='Nome validatore', max_length=128) # dalla piattaforma del CAI
    descrizione = models.CharField(verbose_name='Descrizione', max_length=256)

    data = models.DateField(verbose_name='Data validazione', auto_now=True)
    data_aggiornamento = models.DateField(verbose_name='Data aggiornamento', auto_now=True)

    regione = models.CharField(verbose_name='Regione', max_length=64)
    comunita_montana = models.CharField(verbose_name='Comunità montana', max_length=128)
    gruppo_montuoso = models.CharField(verbose_name='Gruppo montuoso', max_length=128)
    quota = models.IntegerField(verbose_name='Quota')

    class Meta:
        verbose_name = 'Validazione Punto'
        verbose_name_plural = 'Validazione Punti'


class TipoInteresse(models.Model):
    descrizione = models.CharField(verbose_name='Descrizione', max_length=128, unique=True)

    class Meta:
        verbose_name = 'Tipo di Interesse'
        verbose_name_plural = 'Tipi di Interesse'

    def __str__(self):
        return self.descrizione


class InteresseSpecifico(models.Model):
    descrizione = models.CharField(verbose_name='Descrizione', max_length=128, unique=True)
    tipo = models.ForeignKey(TipoInteresse, verbose_name='Tipo', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Interesse Specifico'
        verbose_name_plural = 'Interessi Specifici'

    def __str__(self):
        return self.descrizione


class QualitaInteresse(models.Model):
    descrizione = models.CharField(verbose_name='Descrizione', max_length=128, unique=True)

    class Meta:
        verbose_name = 'Qualità Interesse'
        verbose_name_plural = 'Qualità Interessi'

    def __str__(self):
        return self.descrizione


class EstensioneInteresse(models.Model):
    descrizione = models.CharField(verbose_name='Descrizione', max_length=128, unique=True)

    class Meta:
        verbose_name = 'Estensione Interesse'
        verbose_name_plural = 'Estensione Interessi'

    def __str__(self):
        return self.descrizione
