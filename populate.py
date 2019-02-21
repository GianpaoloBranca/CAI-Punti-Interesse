import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'report.settings')

# pylint: disable=wrong-import-position
import django
django.setup()

# pylint: disable=wrong-import-position
from punti_interesse.models import *

def populate():

    int_cult = ['Borgo', 'Edificio di culto', 'Manufatto', 'Archeosito', 'Museo']
    int_nat = ['Punto panoramico', 'Geosito', 'Biosito vegetazione', 'Biosito flora', 'Biosito fauna']
    degr_amb = ['Incendio', 'Cantiere', 'Frana', 'Inquinamento']
    qualita = ['Raro', 'Esemplificativo', 'Rappresentativo', 'Endemico']
    estensione = ['Locale', 'Ragionale', 'Nazionale', 'Internazionale']

    categorie = {
        'Interesse culturale' : int_cult,
        'Interesse naturalistico/ambientale' : int_nat,
        'Degrado paesaggistico/ambientale' : degr_amb,
    }

    for qual in qualita:
        add_qualita(qual)

    for est in estensione:
        add_estensione(est)

    for cat, subcats in categorie.items():
        categoria = add_cat(cat)
        for subcat in subcats:
            add_subcat(categoria, subcat)

    #default_point_fields = {
    #    'longitudine' : 0.0,
    #    'latitudine' : 0.0,
    #    'categoria' : TipoInteresse.objects.get(descrizione='Interesse Culturale'),
    #    'sottocategoria' : InteresseSpecifico.objects.get(descrizione='Borgo'),
    #    'nome' : 'Punto Vuoto',
    #    'localita' : '.',
    #    'valle' : '.',
    #    'qualita' : QualitaInteresse.objects.get(descrizione='Raro'),
    #    'estensione' : EstensioneInteresse.objects.get(descrizione='Locale'),
    #    'valenza' : '.',
    #    'visitabile' : False,
    #    'visitabile2' : False,
    #    # TODO completare
    #}

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

def add_point(fields):
    punto = PuntoInteresse(fields)
    punto.save()
    return punto

if __name__ == '__main__':
    print('populating the db...')
    populate()
    print('done.')
