from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.forms.models import model_to_dict
from punti_interesse.forms import PuntoInteresseForm
from punti_interesse.models import TipoInteresse, InteresseSpecifico
import populate

class PuntoInteresseFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        populate.populate()
        cls.punto = populate.add_default_point()
        cls.form_args = model_to_dict(cls.punto)
        cls.form_args['nome'] = 'Test point'

    def test_correct_data(self):
        """Se i dati inseriti sono corretti il form deve essere valido"""
        form = PuntoInteresseForm(self.form_args)
        self.assertTrue(form.is_valid())

    def test_unique_name(self):
        """Due punto con lo stesso nome, o con nome che genera lo stesso slug, non possono esistere"""
        self.form_args['nome'] = 'punto-vuoto' # esiste già un poi di nome "Punto Vuoto"
        form = PuntoInteresseForm(self.form_args)
        self.assertFalse(form.is_valid())

    def test_subcategory_consistency(self):
        """La sottocategoria di un punto deve appartenere alla sua categoria"""
        self.form_args['categoria'] = TipoInteresse.objects.get_or_create(descrizione='Interesse culturale')[0].id
        self.form_args['sottocategoria'] = InteresseSpecifico.objects.get_or_create(descrizione='Frana')[0].id
        form = PuntoInteresseForm(self.form_args)
        self.assertFalse(form.is_valid())
