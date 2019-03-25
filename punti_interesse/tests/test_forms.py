from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.forms.models import model_to_dict
from punti_interesse.forms import PuntoInteresseForm, ValidazioneForm
from punti_interesse.models import TipoInteresse, InteresseSpecifico
import populate

class PuntoInteresseFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        populate.populate()
        cls.punto = populate.add_default_point()

    def setUp(self):
        self.form_args = model_to_dict(self.punto)
        self.form_args['nome'] = 'Test point'

    def test_correct_data(self):
        """Se i dati inseriti sono corretti il form deve essere valido"""
        form = PuntoInteresseForm(self.form_args)
        self.assertTrue(form.is_valid())

    def test_unique_name(self):
        """Due punto con lo stesso nome, o con nome che genera lo stesso slug, non possono esistere"""
        self.form_args['nome'] = 'punto-vuoto' # esiste già un poi di nome "Punto Vuoto"
        form = PuntoInteresseForm(self.form_args)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_subcategory_consistency(self):
        """La sottocategoria di un punto deve appartenere alla sua categoria"""
        self.form_args['categoria'] = TipoInteresse.objects.get_or_create(descrizione='Interesse culturale')[0].id
        self.form_args['sottocategoria'] = InteresseSpecifico.objects.get_or_create(descrizione='Frana')[0].id
        form = PuntoInteresseForm(self.form_args)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_visitability_for_disable(self):
        """Un punto di interesse non può essere visitabile solo da disabili"""
        self.form_args['visitabile'] = False
        self.form_args['visitabile2'] = True
        form = PuntoInteresseForm(self.form_args)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_coordinates(self):
        """Longitudine e latitudine devono avere un valore compreso tra -180 e 180"""
        self.form_args['longitudine'] = 232.98
        self.form_args['latitudine'] = -623.30
        form = PuntoInteresseForm(self.form_args)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)


class ValidazioneFormTest(TestCase):

    def setUp(self):
        self.form_args = {
            'regione' : 'LOM',
            'comunita_montana' : 'Qualsiasi',
            'gruppo_montuoso' : 'Dolomiti',
            'quota' : 1550,
            'descrizione' : 'esempio'
        }

    def test_correct_data(self):
        """Se i dati inseriti sono corretti il form deve essere valido"""
        form = ValidazioneForm(self.form_args)
        self.assertTrue(form.is_valid())

    def test_invalid_quota(self):
        """La quota inserita deve essere maggiore o uguale a zero"""
        self.form_args['quota'] = -87
        form = ValidazioneForm(self.form_args)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_invalid_regione(self):
        """La regione deve essere una di quelle presenti"""
        self.form_args['regione'] = 'MAH'
        form = ValidazioneForm(self.form_args)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
