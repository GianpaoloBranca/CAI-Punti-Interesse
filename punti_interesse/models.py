from django.db import models
from django.template.defaultfilters import slugify
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from punti_interesse.validators import validate_degree, MaxSizeValidator, validate_punto_rilevatore, validate_punto_validatore

class PuntoInteresse(models.Model):
    longitudine = models.DecimalField(verbose_name='Longitudine*', max_digits=9, decimal_places=6, validators=[validate_degree])
    latitudine = models.DecimalField(verbose_name='Latitudine*', max_digits=9, decimal_places=6, validators=[validate_degree])

    categoria = models.ForeignKey('TipoInteresse', verbose_name='Tipologia*', on_delete=models.PROTECT)
    sottocategoria = models.ForeignKey('InteresseSpecifico', verbose_name='Oggetto Specifico*', on_delete=models.PROTECT)

    nome = models.CharField(verbose_name='Nome*', max_length=50)
    localita = models.CharField(verbose_name='Località*', max_length=75)
    valle = models.CharField(verbose_name='Valle', max_length=75, blank=True)
    qualita = models.ForeignKey('QualitaInteresse', verbose_name='Qualità Interesse*', on_delete=models.PROTECT)
    estensione = models.ForeignKey('EstensioneInteresse', verbose_name='Estensione Interesse*', on_delete=models.PROTECT)

    valenza = models.CharField(verbose_name='Titolo della valenza*', max_length=30)
    visitabile = models.BooleanField(verbose_name='Visitabile*')
    visitabile2 = models.BooleanField(verbose_name='Visitabile per persone con ridotta capacità motoria o sensoriale*')
    periodo = models.CharField(verbose_name='Periodo di visita consigliato', max_length=50, blank=True)
    istituto = models.CharField(verbose_name='Istituto di tutela', max_length=50, blank=True)

    foto_copertina = models.ImageField(verbose_name='Foto copertina*', upload_to='foto_copertina/', validators=[MaxSizeValidator(2)])

    descr_breve = models.TextField(verbose_name='Descrizione oggetto breve*', max_length=256)
    descr_estesa = models.TextField(verbose_name='Descrizione oggetto estesa*', max_length=1024)
    descr_sito = models.TextField(verbose_name='Descrizione sito*', max_length=256)

    stato_conservazione = models.ForeignKey('StatoConservazione', verbose_name='Stato Conservazione*', on_delete=models.PROTECT, default=2) # 2 = normale

    motivo = models.TextField(verbose_name='Motivo per la fruizione', max_length=256, blank=True)

    rif_biblio = models.TextField(verbose_name='Riferimenti bibliografici', max_length=256, blank=True)
    rif_sito = models.TextField(verbose_name='Riferimenti sitografici', max_length=256, blank=True)

    rilevatore = models.ForeignKey(User, verbose_name='Utente rilevatore', on_delete=models.SET_NULL, null=True, validators=[validate_punto_rilevatore])

    data = models.DateField(verbose_name='Data inserimento', auto_now=True)
    validato = models.BooleanField(verbose_name='Validato', default=False)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Punto di Interesse'
        verbose_name_plural = 'Punti di Interesse'

    def __str__(self):
        return self.nome

    #pylint: disable=arguments-differ
    def save(self, *args, **kwargs):
        self.slug = slugify(self.nome)
        super(PuntoInteresse, self).save(*args, **kwargs)

    def clean(self):
        self._check_unique_name()
        self._check_subcategory_consistency()
        self._check_visitability_consistency()

    def _check_subcategory_consistency(self):
        if self.sottocategoria.tipo != self.categoria:
            raise ValidationError({"sottocategoria" : "Questo campo non appartiene alla Tipologia corretta"})

    def _check_unique_name(self):
        slug = slugify(self.nome)
        if PuntoInteresse.objects.exclude(id=self.id).filter(slug=slug).exists():
            raise ValidationError({"nome" : "Nome già utilizzato"})

    def _check_visitability_consistency(self):
        if not self.visitabile and self.visitabile2:
            raise ValidationError({"visitabile2" : "Il punto di interesse non può essere visitabile solo per persone con disabilità"})


class ValidazionePunto(models.Model):
    punto = models.OneToOneField(PuntoInteresse, on_delete=models.CASCADE, primary_key=True)
    validatore = models.ForeignKey(User, verbose_name='Utente validatore', on_delete=models.SET_NULL, null=True, validators=[validate_punto_validatore])

    descrizione = models.TextField(verbose_name='Descrizione*', max_length=256)
    data_aggiornamento = models.DateField(verbose_name='Data aggiornamento', auto_now=True)

    LISTA_REGIONI = (
        ("VDA", "Valle d'Aosta"),
        ("PIE", "Piemonte"),
        ("LIG", "Liguria"),
        ("LOM", "Lombardia"),
        ("TAA", "Trentino Alto Adige"),
        ("VEN", "Veneto"),
        ("FVG", "Friuli Venezia Giulia"),
        ("ERM", "Emilia Romagna"),
        ("TOS", "Toscana"),
        ("UMB", "Umbria"),
        ("MAR", "Marche"),
        ("LAZ", "Lazio"),
        ("ABR", "Abruzzo"),
        ("MOL", "Molise"),
        ("CAM", "Campania"),
        ("PUG", "Puglia"),
        ("BAS", "Basilicata"),
        ("CAL", "Calabria"),
        ("SIC", "Sicilia"),
        ("SAR", "Sardegna")
    )

    regione = models.CharField(verbose_name='Regione*', max_length=30, choices=LISTA_REGIONI)
    comunita_montana = models.CharField(verbose_name='Comunità montana', max_length=128, blank=True)
    gruppo_montuoso = models.ForeignKey('GruppoMontuoso', verbose_name='Gruppo Montuoso', on_delete=models.PROTECT, null=True, blank=True)

    quota = models.DecimalField(verbose_name='Quota*', max_digits=4, decimal_places=0, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'Validazione Punto'
        verbose_name_plural = 'Validazione Punti'

    def __str__(self):
        return str(self.punto)


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


class StatoConservazione(models.Model):
    descrizione = models.CharField(verbose_name='Descrizione', max_length=128, unique=True)

    class Meta:
        verbose_name = 'Stato di Conservazione'
        verbose_name_plural = 'Stati di Conservazione'

    def __str__(self):
        return self.descrizione


class FotoAccessoria(models.Model):
    punto = models.ForeignKey(PuntoInteresse, on_delete=models.CASCADE)
    foto = models.ImageField(verbose_name='Foto', upload_to='foto_accessorie/', validators=[MaxSizeValidator(1)])

    class Meta:
        verbose_name = 'Foto Accessoria'
        verbose_name_plural = 'Foto Accessorie'

    def __str__(self):
        return str(self.punto)


class GruppoMontuoso(models.Model):
    nome = models.CharField(verbose_name='Nome', max_length=50)

    class Meta:
        verbose_name = 'Gruppo Montuoso'
        verbose_name_plural = 'Gruppi Montuosi'

    def __str__(self):
        return self.nome


# Not sure it's needed
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extra')
    uuid = models.CharField(verbose_name='UUID', max_length=64)
    sectioncode = models.IntegerField(verbose_name='Codice Sezione')

    class Meta:
        verbose_name = 'Informazioni Aggiuntive Utenti'
        verbose_name_plural = 'Informazioni Aggiuntive Utenti'

    def __str__(self):
        return str(self.user)
