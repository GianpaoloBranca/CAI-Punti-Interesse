import os
import sys
import csv
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'report.settings')

# pylint: disable=wrong-import-position
import django
django.setup()

# pylint: disable=wrong-import-position
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
from punti_interesse.models import *


def populate():

    int_cult = ['Borgo', 'Edificio di culto', 'Manufatto', 'Archeosito', 'Museo']
    int_nat = ['Punto panoramico', 'Geosito', 'Biosito vegetazione', 'Biosito flora', 'Biosito fauna']
    degr_amb = ['Incendio', 'Cantiere', 'Frana', 'Inquinamento']
    qualita = ['Raro', 'Esemplificativo', 'Rappresentativo', 'Endemico']
    estensione = ['Locale', 'Regionale', 'Nazionale', 'Internazionale']
    stati_conservazione = ['Povero', 'Normale', 'Buono'] # valori temporanei
    groups = ['Rilevatore', 'Validatore']

    categorie = {
        'Interesse culturale' : int_cult,
        'Interesse naturalistico/ambientale' : int_nat,
        'Degrado paesaggistico/ambientale' : degr_amb,
    }

    for qual in qualita:
        add_qualita(qual)

    for est in estensione:
        add_estensione(est)

    for stato in stati_conservazione:
        add_statoconservazione(stato)

    for cat, subcats in categorie.items():
        categoria = add_cat(cat)
        for subcat in subcats:
            add_subcat(categoria, subcat)

    for group in groups:
        add_group(group)

def add_cat(descr):
    cat = TipoInteresse.objects.get_or_create(descrizione=descr)[0]
    cat.save()
    return cat

def add_subcat(cat, descr):
    subcat = InteresseSpecifico.objects.get_or_create(tipo=cat, descrizione=descr)[0]
    subcat.save()
    return subcat

def add_qualita(descr):
    qual = QualitaInteresse.objects.get_or_create(descrizione=descr)[0]
    qual.save()
    return qual

def add_estensione(descr):
    est = EstensioneInteresse.objects.get_or_create(descrizione=descr)[0]
    est.save()
    return est

def add_statoconservazione(descr):
    stato = StatoConservazione.objects.get_or_create(descrizione=descr)[0]
    stato.save()
    return stato

def add_group(name):
    group = Group.objects.get_or_create(name=name)[0]
    group.save()
    return group

def add_point(fields):
    punto = PuntoInteresse.objects.create(**fields)
    return punto

def add_default_point():
    try:
        return add_point(get_default_point_fields())
    except ObjectDoesNotExist:
        print("Missing objects in related tables. Did you forget to call populate() first?")

def get_default_point_fields():
    default_point_fields = {
        'longitudine' : 0.0,
        'latitudine' : 0.0,
        'categoria' : TipoInteresse.objects.get(descrizione='Interesse culturale'),
        'sottocategoria' : InteresseSpecifico.objects.get(descrizione='Borgo'),
        'nome' : 'Punto Vuoto',
        'localita' : '.',
        'valle' : '.',
        'qualita' : QualitaInteresse.objects.get(descrizione='Raro'),
        'estensione' : EstensioneInteresse.objects.get(descrizione='Locale'),
        'valenza' : '.',
        'visitabile' : False,
        'visitabile2' : False,
        'periodo' : '.',
        'istituto': '.',
        'foto_copertina': '.',
        'descr_breve' : '.',
        'descr_estesa' : '.',
        'descr_sito' : '.',
        'motivo' : '.',
        'rif_biblio' : '.',
        'rif_sito' : '.',
    }
    return default_point_fields

def add_gruppi_montuosi(filepath):
    """Carica i gruppi montuosi nel db da un file csv"""
    with open(filepath, 'r', encoding='latin-1') as csvfile:
        gm_reader = csv.reader(csvfile)
        next(gm_reader) # skip header line

        for row in gm_reader:
            nome_gruppo_montuoso = ''.join(row)
            if nome_gruppo_montuoso != '':
                gruppo_montuoso = GruppoMontuoso.objects.get_or_create(nome=nome_gruppo_montuoso)[0]
                gruppo_montuoso.save()


if __name__ == '__main__':
    if sys.argv[1] == '-gm':
        add_gruppi_montuosi(sys.argv[2])
    else:
        print('populating the db...')
        populate()
        print('done.')
