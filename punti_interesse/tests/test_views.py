from unittest import skip
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User, AnonymousUser, Group
from django.forms.models import model_to_dict
from django.urls import reverse
from punti_interesse import views
from punti_interesse.models import PuntoInteresse, UserInfo, ValidazionePunto, InteresseSpecifico
import populate

class ViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        populate.populate()
        cls.group_r = Group.objects.get(name='Rilevatore')
        cls.group_v = Group.objects.get(name='Validatore')
        cls.factory = RequestFactory()
        cls.user = User.objects.create_user(username='user', password='secret')
        UserInfo.objects.create(user=cls.user, uuid='oerinvqo', sectioncode=123)
        cls.request = cls.factory.get(reverse('home'))
        cls.punto = populate.add_default_point()
        cls.punto.rilevatore = cls.user
        cls.punto.save()

    def setUp(self):
        self.user.is_superuser = False
        self.user_is_staff = False
        self.user.groups.clear()
        self.request.user = self.user

    # ---------- Homepage -------------

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

    # ---------- Show page ------------

    def test_show(self):
        """Se il punto esiste il server restituisce la pagina con tutte le sue informazioni"""
        response = views.show(self.request, self.punto.slug)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.punto.nome)

    def test_show_punto_does_not_exists(self):
        """Se il punto di interesse non esiste il server restituisce la pagina di errore 404"""
        response = views.show(self.request, 'invalid-slug')
        self.assertEqual(response.status_code, 404)

    # ---------- New page -------------

    def test_new(self):
        self.user.groups.add(self.group_r)
        response = views.new(self.request)
        self.assertEqual(response.status_code, 200)

    def test_new_user_is_not_rilevatore(self):
        response = views.new(self.request)
        response.client = Client()
        self.assertEqual(response.status_code, 403)

    @skip('skipping post requests for now')
    def test_new_post(self):
        # Non usa la request della classe di test ma una diversa (post)
        request = self.factory.post(reverse('new'))
        post_dict = model_to_dict(self.punto)
        post_dict['nome'] = 'nuovo nome'
        request.POST = post_dict
        with open('static/images/placeholder.jpg', 'rb') as uploaded_image:
            request.FILES['foto_copertina'] = uploaded_image
            request.FILES['foto_copertina'].read()
        self.user.groups.add(self.group_r)
        request.user = self.user
        response = views.new(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PuntoInteresse.objects.all().count(), 2)
        PuntoInteresse.objects.get(nome='nuovo nome').delete()

    # ---------- Edit page ------------

    def test_edit(self):
        self.user.groups.add(self.group_r)
        response = views.edit(self.request, self.punto.slug)
        self.assertEqual(response.status_code, 200)

    def test_edit_user_is_not_owner(self):
        self.user.groups.add(self.group_r)
        self.user.extra.uuid = 'mismatch'
        response = views.edit(self.request, self.punto.slug)
        self.assertEqual(response.status_code, 403)

    def test_edit_user_is_not_rilevatore(self):
        response = views.edit(self.request, self.punto.slug)
        response.client = Client()
        self.assertEqual(response.status_code, 403)

    def test_edit_punto_does_not_esists(self):
        self.user.groups.add(self.group_r)
        response = views.edit(self.request, 'invalid-slug')
        self.assertEqual(response.status_code, 404)

    @skip('skipping post requests for now')
    def test_edit_post(self):
        pass

    # ------- Validation page ---------

    def test_validate(self):
        self.user.groups.add(self.group_v)
        response = views.validate(self.request, self.punto.slug)
        self.assertEqual(response.status_code, 200)

    def test_validate_user_is_not_validatore(self):
        self.user.groups.add(self.group_r)
        response = views.validate(self.request, self.punto.slug)
        response.client = Client()
        self.assertEqual(response.status_code, 403)

    def test_validate_punto_does_not_exists(self):
        self.user.groups.add(self.group_v)
        response = views.validate(self.request, '')
        self.assertEqual(response.status_code, 404)

    def test_validate_post(self):
        self.user.groups.add(self.group_v)
        request = self.factory.post(reverse('validate', kwargs={'slug' : self.punto.slug}))
        request.POST = {
            'regione' : 'LOM',
            'quota' : 1500,
            'descrizione' : 'testo'
        }
        request.user = self.user
        response = views.validate(request, self.punto.slug)
        self.assertEqual(response.status_code, 302)
        val = ValidazionePunto.objects.get(punto=self.punto)
        self.assertEqual(val.punto, self.punto)
        val.delete()

    # ------- Admin functions ---------

    def test_remove_invalid_points(self):
        self.user.is_staff = True
        self.user.is_superuser = True
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
        response = views.export_csv(self.request)
        self.assertEqual(response.get('Content-Type'), 'text/csv')
        self.assertEqual(response.get('Content-Disposition'), 'attachment; filename="punti.csv"')

    def test_csv_iterator(self):
        iterator = views.csv_iterator()
        self.assertEqual(next(iterator), ('Nome', 'Latitudine', 'Longitudine', 'Categoria', 'Sottocategoria'))
        self.assertEqual(next(iterator), (self.punto.nome, self.punto.latitudine, self.punto.longitudine, str(self.punto.categoria), str(self.punto.sottocategoria)))

    # ---------- Ajax function --------

    def test_load_subcategory(self):
        request = self.factory.get(reverse('ajax_load_subcategories'))
        cat = self.punto.categoria.id
        request.GET = {'categoria' : cat}
        response = views.load_subcategories(request)
        n_options = InteresseSpecifico.objects.filter(tipo=cat).count()
        # plus 1 for the unselected option, times 2 for closing tag
        self.assertContains(response, 'option', count=(n_options+1)*2)
        self.assertContains(response, str(self.punto.sottocategoria))

    def test_load_subcategory_invalid_category(self):
        request = self.factory.get(reverse('ajax_load_subcategories'))
        request.GET = {'categoria' : 619}
        response = views.load_subcategories(request)
        # has only the unselected option
        self.assertContains(response, 'option', count=2)

    def test_load_subcategory_string_category(self):
        request = self.factory.get(reverse('ajax_load_subcategories'))
        request.GET = {'categoria' : 'something'}
        response = views.load_subcategories(request)
        # has only the unselected option
        self.assertContains(response, 'option', count=2)

    # ---------- Error pages ----------

    def test_error_404(self):
        response = views.handler404(self.request, None)
        self.assertEqual(response.status_code, 404)

    def test_error_500(self):
        response = views.handler500(self.request)
        self.assertEqual(response.status_code, 500)
