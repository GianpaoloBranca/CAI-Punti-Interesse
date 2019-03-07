from django_cas_ng.signals import cas_user_authenticated
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from punti_interesse.templatetags.pi_template_tags import is_rilevatore, is_validatore
import report.settings

@receiver(cas_user_authenticated)
def cas_login_callback(sender, **kwargs):

    attributes = kwargs.get('attributes')

    if report.settings.DEBUG:
        print('login successful')
        print(attributes)

    if attributes:

        email = attributes.get('email')
        roles = attributes.get('roles')

        if email:
            user, _ = User.objects.get_or_create(username=email)
            user.first_name = attributes.get('firstname', '')
            user.last_name = attributes.get('lastname', '')
            user.email = email

            user.groups.clear()
            if roles:
                # Expects roles to be passed as 'ROLE_A,ROLE_B,...'
                roles_list = roles.split(',')

                if 'ROLE_POI_ADMIN' in roles_list:
                    user.is_superuser = True
                    user.is_staff = True
                else:
                    user.is_superuser = False
                    user.is_staff = False

                if 'ROLE_POI_RILEVATORE' in roles_list:
                    rilevatore = Group.objects.get(name='Rilevatore')
                    user.groups.add(rilevatore)

                if 'ROLE_POI_VALIDATORE' in roles_list:
                    validatore = Group.objects.get(name='Validatore')
                    user.groups.add(validatore)

            user.save()
