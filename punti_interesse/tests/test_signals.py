from django.test import TestCase
from django.contrib.auth.models import User, Group
from punti_interesse.signals.cas_handlers import cas_login_callback
from punti_interesse.templatetags.pi_template_tags import is_rilevatore, is_validatore

class CasLoginCallbackTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Group.objects.create(name='Rilevatore')
        Group.objects.create(name='Validatore')
        cls.user = User.objects.create_user(username='user', password='secret')

    def setUp(self):
        self.attributes = {
            'uuid' : '2039r29nd2i384n',
            'sectioncode' : 12345,
            'roles' : '',
        }
        self.kwargs = {
            'attributes' : self.attributes,
            'user' : self.user
        }

    def test_login_default(self):
        cas_login_callback(None, **self.kwargs)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertFalse(is_rilevatore(self.user))
        self.assertFalse(is_validatore(self.user))

    def test_login_extra_attributes(self):
        cas_login_callback(None, **self.kwargs)
        self.assertEqual(self.user.extra.uuid, '2039r29nd2i384n')
        self.assertEqual(self.user.extra.sectioncode, 12345)

    def test_login_admin(self):
        self.attributes['roles'] = 'ROLE_POI_ADMIN'
        cas_login_callback(None, **self.kwargs)
        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.is_superuser)
        self.assertFalse(is_rilevatore(self.user))
        self.assertFalse(is_validatore(self.user))

    def test_login_rilevatore(self):
        self.attributes['roles'] = 'ROLE_POI_RILEVATORE'
        cas_login_callback(None, **self.kwargs)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertTrue(is_rilevatore(self.user))
        self.assertFalse(is_validatore(self.user))

    def test_login_validatore(self):
        self.attributes['roles'] = 'ROLE_POI_VALIDATORE'
        cas_login_callback(None, **self.kwargs)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertFalse(is_rilevatore(self.user))
        self.assertTrue(is_validatore(self.user))
