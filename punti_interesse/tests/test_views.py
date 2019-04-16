from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse
from punti_interesse.views import home

class ViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.user = User.objects.create_user(username='user', password='secret')

    def test_access_granted(self):
        """Gli utenti registrati devono poter accedere all'applicazione"""
        request = self.factory.get(reverse('home'))
        request.user = self.user
        response = home(request)
        self.assertEqual(response.status_code, 200)

    def test_access_denied(self):
        """Gli utenti non registrati vengono rimandati alla pagina di login"""
        request = self.factory.get(reverse('home'))
        request.user = AnonymousUser()
        response = home(request)
        response.client = Client()
        self.assertRedirects(response, reverse('cas_ng_login') + '?next=' + reverse('home'), target_status_code=302)
