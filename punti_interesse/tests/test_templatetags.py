from django.test import TestCase
from django.contrib.auth.models import User, Group
from punti_interesse.templatetags import pi_template_tags as tags

class TemplateTagsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user', password='secret')

    def test_user_is_rilevatore(self):
        """Il tag restituisce True se l'utente è un rilevatore, False altrimenti"""
        group_rilevatore = Group.objects.create(name='Rilevatore')
        self.assertFalse(tags.is_rilevatore(self.user))
        self.user.groups.add(group_rilevatore)
        self.assertTrue(tags.is_rilevatore(self.user))

    def test_user_is_validatore(self):
        """Il tag restituisce True se l'utente è un validatore, False altrimenti"""
        group_validatore = Group.objects.create(name='Validatore')
        self.assertFalse(tags.is_validatore(self.user))
        self.user.groups.add(group_validatore)
        self.assertTrue(tags.is_validatore(self.user))

    def test_markup_no_italic(self):
        """Il testo non contienente codice per il corsivo non deve essere alterato"""
        message = "Questo testo non deve essere alterato."
        self.assertEqual(tags.markup(message), message)

    def test_markup_italic(self):
        """Il testo contienente codice per il corsivo, deve essere modificato con <i> e </i>"""
        message = "Questo testo **deve** essere alterato."
        self.assertEqual(tags.markup(message), "Questo testo <i>deve</i> essere alterato.")

    def test_markup_wrong_number_of_asteriscs(self):
        """Il testo con un markup per il corsivo errato deve restituire un testo html con tag compatibili"""
        message = "*Questo ***testo* fa** cose stra**ne."
        self.assertEqual(tags.markup(message), "*Questo <i>*testo* fa</i> cose stra**ne.")
