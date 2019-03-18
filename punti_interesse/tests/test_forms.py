from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.forms.models import model_to_dict
from punti_interesse.forms import PuntoInteresseForm
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
