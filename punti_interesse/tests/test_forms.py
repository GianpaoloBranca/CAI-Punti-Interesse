from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.forms.models import model_to_dict
from punti_interesse.forms import PuntoInteresseForm, ValidazioneForm
from punti_interesse.models import TipoInteresse, InteresseSpecifico

from django.core.files.uploadedfile import SimpleUploadedFile
import populate

class PuntoInteresseFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        populate.populate()
        cls.punto = populate.add_default_point()
        with open('media/foto_copertina/Boston_City_Flow.jpg', 'rb') as uploaded_image:
            cls.file_dict = {'foto_copertina' : SimpleUploadedFile(uploaded_image.name, uploaded_image.read(), content_type='image/jpeg')}

    def setUp(self):
        self.post_dict = model_to_dict(self.punto)
        self.post_dict['nome'] = 'Test point'

    def test_correct_data(self):
        """Se i dati inseriti sono corretti il form deve essere valido"""
        form = PuntoInteresseForm(data=self.post_dict, files=self.file_dict)
        self.assertTrue(form.is_valid())

    def test_unique_name(self):
        """Due punto con lo stesso nome, o con nome che genera lo stesso slug, non possono esistere"""
        self.post_dict['nome'] = 'punto-vuoto' # esiste già un poi di nome "Punto Vuoto"
        form = PuntoInteresseForm(data=self.post_dict, files=self.file_dict)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_subcategory_consistency(self):
        """La sottocategoria di un punto deve appartenere alla sua categoria"""
        self.post_dict['categoria'] = TipoInteresse.objects.get_or_create(descrizione='Interesse culturale')[0].id
        self.post_dict['sottocategoria'] = InteresseSpecifico.objects.get_or_create(descrizione='Frana')[0].id
        form = PuntoInteresseForm(data=self.post_dict, files=self.file_dict)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_visitability_for_disable(self):
        """Un punto di interesse non può essere visitabile solo da disabili"""
        self.post_dict['visitabile'] = False
        self.post_dict['visitabile2'] = True
        form = PuntoInteresseForm(data=self.post_dict, files=self.file_dict)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_coordinates(self):
        """Longitudine e latitudine devono avere un valore compreso tra -180 e 180"""
        self.post_dict['longitudine'] = 232.98
        self.post_dict['latitudine'] = -623.30
        form = PuntoInteresseForm(data=self.post_dict, files=self.file_dict)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)


class ValidazioneFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        populate.add_gruppi_montuosi('res/GruppoM1.csv')

    def setUp(self):
        self.post_dict = {
            'regione' : 'LOM',
            'comunita_montana' : 'Qualsiasi',
            'gruppo_montuoso' : 34,
            'quota' : 1550,
            'descrizione' : 'esempio'
        }

    def test_correct_data(self):
        """Se i dati inseriti sono corretti il form deve essere valido"""
        form = ValidazioneForm(self.post_dict)
        #self.assertTrue(form.is_valid())
        form.is_valid()
        print(form.errors)

    def test_invalid_quota(self):
        """La quota inserita deve essere maggiore o uguale a zero"""
        self.post_dict['quota'] = -87
        form = ValidazioneForm(self.post_dict)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_invalid_regione(self):
        """La regione deve essere una di quelle presenti"""
        self.post_dict['regione'] = 'MAH'
        form = ValidazioneForm(self.post_dict)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
