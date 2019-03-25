from unittest import skip
from django.test import TestCase

from django.core.exceptions import ValidationError

from punti_interesse.models import PuntoInteresse, TipoInteresse, InteresseSpecifico
from populate import populate, add_default_point, get_default_point_fields

class PuntoInteresseTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        populate()
        cls.punto = add_default_point()

    @skip("La validazione a livello di form dovrebbe essere sufficiente")
    def test_unique_name(self):
        """Due punto con lo stesso nome, o con nome che genera lo stesso slug, non possono esistere"""
        punto2 = PuntoInteresse(**get_default_point_fields())
        # Il nome del punto di default è "Punto Vuoto"
        punto2.nome = 'punto-vuoto'
        self.assertRaises(ValidationError, punto2.save)
        punto2.nome = 'Altro punto'
        punto2.save()

    @skip("La validazione a livello di form dovrebbe essere sufficiente")
    def test_subcategory_consistency(self):
        """La sottocategoria di un punto deve appartenere alla sua categoria"""
        self.punto.categoria = TipoInteresse.objects.get(descrizione='Interesse culturale')
        self.punto.sottocategoria = InteresseSpecifico.objects.get(descrizione='Frana')
        # Frana non è nella categoria Interesse culturale
        self.assertRaises(ValidationError, self.punto.save)
        # Imposto la categoria corretta
        self.punto.categoria = TipoInteresse.objects.get(descrizione='Degrado paesaggistico/ambientale')
        self.punto.save()
