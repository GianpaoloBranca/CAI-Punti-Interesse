from django.db import models

class TipoInteresse(models.Model):
    descrizione = models.CharField(verbose_name='Descrizione', max_length=128, unique=True)

    class Meta:
        verbose_name = 'Tipo di Interesse'
        verbose_name_plural = 'Tipi di Interesse'

    def __str__(self):
        return self.descrizione


class InteresseSpecifico(models.Model):
    descrizione = models.CharField(verbose_name='Descrizione', max_length=128, unique=True)
    tipo = models.ForeignKey(TipoInteresse, on_delete=models.CASCADE)

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
