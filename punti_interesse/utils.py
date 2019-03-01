from punti_interesse.models import PuntoInteresse, InteresseSpecifico, TipoInteresse

# pylint: disable=too-few-public-methods
class Echo:
    # pylint: disable=no-self-use
    def write(self, value):
        return value


def csv_iterator():

    cats = dict((c.id, c.descrizione) for c in TipoInteresse.objects.all())
    subcats = dict((s.id, s.descrizione) for s in InteresseSpecifico.objects.all())
    points = PuntoInteresse.objects.values_list('nome', 'latitudine', 'longitudine', 'categoria', 'sottocategoria')

    yield ('Nome', 'Latitudine', 'Longitudine', 'Categoria', 'Sottocategoria')

    for punto in points:
        yield (punto[0], punto[1], punto[2], cats[punto[3]], subcats[punto[4]])
