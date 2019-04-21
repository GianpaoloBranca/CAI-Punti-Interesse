from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User, AnonymousUser, Group
from django.urls import reverse
from punti_interesse import views
from punti_interesse.models import PuntoInteresse
import populate

class ViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        populate.populate()
        cls.group_r = Group.objects.get(name='Rilevatore')
        cls.group_v = Group.objects.get(name='Validatore')
        cls.factory = RequestFactory()
        cls.user = User.objects.create_user(username='user', password='secret')
        cls.request = cls.factory.get(reverse('home'))
        cls.punto = populate.add_default_point()
        cls.punto.rilevatore = cls.user
        cls.punto.save()

    def setUp(self):
        self.user.is_superuser = False
        self.user_is_staff = False
        self.user.groups.clear()
        self.request.user = self.user

    def test_home_access_granted(self):
        """Gli utenti registrati devono poter accedere all'applicazione"""
        response = views.home(self.request)
        self.assertEqual(response.status_code, 200)

    def test_home_access_denied(self):
        """Gli utenti non registrati vengono rimandati alla pagina di login"""
        self.request.user = AnonymousUser()
        response = views.home(self.request)
        response.client = Client()
        self.assertRedirects(response, reverse('cas_ng_login') + '?next=' + reverse('home'), target_status_code=302)

    def test_show(self):
        """Se il punto esiste il server restituisce la pagina con tutte le sue informazioni"""
        response = views.show(self.request, self.punto.slug)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.punto.nome)

    def test_show_punto_does_not_exists(self):
        """Se il punto di interesse non esiste il server restituisce la pagina di errore 404"""
        response = views.show(self.request, 'invalid-slug')
        self.assertEqual(response.status_code, 404)

    def test_new(self):
        self.user.groups.add(self.group_r)
        response = views.new(self.request)
        self.assertEqual(response.status_code, 200)

    def test_new_forbidden_access(self):
        response = views.new(self.request)
        response.client = Client()
        self.assertRedirects(response, reverse('cas_ng_login') + '?next=' + reverse('home'), target_status_code=302)

    def test_remove_invalid_points(self):
        self.user.is_staff = True
        self.user.is_superuser = True
        self.request.user = self.user
        response = views.remove_invalid_points(self.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PuntoInteresse.objects.all().count(), 0)
        # Restore deleted point
        self.punto = populate.add_default_point()
        self.punto.rilevatore = self.user
        self.punto.save()

    def test_remove_invalid_points_but_point_is_valid(self):
        self.user.is_staff = True
        self.user.is_superuser = True
        self.request.user = self.user
        self.punto.validato = True
        self.punto.save()
        response = views.remove_invalid_points(self.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PuntoInteresse.objects.all().count(), 1)
        # Restore original information
        self.punto.validato = False
        self.punto.save()

    def test_export_csv(self):
        self.user.is_staff = True
        self.user.is_superuser = True
        self.request.user = self.user
        response = views.export_csv(self.request)
        self.assertEqual(response.get('Content-Type'), 'text/csv')
        self.assertEqual(response.get('Content-Disposition'), 'attachment; filename="punti.csv"')

    def test_csv_iterator(self):
        iterator = views.csv_iterator()
        self.assertEqual(next(iterator), ('Nome', 'Latitudine', 'Longitudine', 'Categoria', 'Sottocategoria'))
        self.assertEqual(next(iterator), (self.punto.nome, self.punto.latitudine, self.punto.longitudine, str(self.punto.categoria), str(self.punto.sottocategoria)))

    def test_error_404(self):
        response = views.handler404(self.request, None)
        self.assertEqual(response.status_code, 404)

    def test_error_500(self):
        response = views.handler500(self.request)
        self.assertEqual(response.status_code, 500)
