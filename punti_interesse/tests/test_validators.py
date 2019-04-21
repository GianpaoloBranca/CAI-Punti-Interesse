from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group

from punti_interesse import validators

class ValidateDegreeTest(TestCase):
    """Testa il metodo validate_degree"""

    def test_valid_value(self):
        """Il valore validato deve essere compreso tra -180 e 180"""
        self.assertIsNone(validators.validate_degree(54.347))

    def test_invalid_value(self):
        """Il valore validato non può essere minore di -180 o maggiore di 180"""
        self.assertRaises(ValidationError, validators.validate_degree, 180.019)

    def test_invalid_type(self):
        """Il valore validato deve essere un numero"""
        self.assertRaises(TypeError, validators.validate_degree, '90.0')


class ValidateUserGroupTest(TestCase):
    """Testa i metodi validate_punto_rilevatore e validate_punto_validatore"""

    @classmethod
    def setUpTestData(cls):
        cls.group_r = Group.objects.create(name='Rilevatore')
        cls.group_v = Group.objects.create(name='Validatore')
        cls.user = User.objects.create_user(username='user', password='secret')

    def setUp(self):
        self.user.groups.clear()

    def test_user_is_default(self):
        """Un utente in nessun gruppo non può essere impostato come rilevatore ne validatore"""
        self.assertRaises(ValidationError, validators.validate_punto_rilevatore, self.user.id)
        self.assertRaises(ValidationError, validators.validate_punto_validatore, self.user.id)

    def test_user_is_rilevatore(self):
        """Un utente rilevatore può essere impostato come rilevatore (ma non come validatore)"""
        self.user.groups.add(self.group_r)
        self.assertIsNone(validators.validate_punto_rilevatore(self.user.id))
        self.assertRaises(ValidationError, validators.validate_punto_validatore, self.user.id)

    def test_user_is_validatore(self):
        """Un utente rilevatore può essere impostato come validatore (ma non come rilevatore)"""
        self.user.groups.add(self.group_v)
        self.assertIsNone(validators.validate_punto_validatore(self.user.id))
        self.assertRaises(ValidationError, validators.validate_punto_rilevatore, self.user.id)

    def test_user_is_superuser(self):
        """Un superutente può essere impostato sia come rilevatore sia come validatore"""
        self.user.is_superuser = True
        self.user.save()
        self.assertIsNone(validators.validate_punto_rilevatore(self.user.id))
        self.assertIsNone(validators.validate_punto_validatore(self.user.id))
