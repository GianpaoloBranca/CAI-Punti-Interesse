from django_cas_ng.signals import cas_user_authenticated
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from punti_interesse.templatetags.pi_template_tags import is_rilevatore, is_validatore
import report.settings

@receiver(cas_user_authenticated)
def cas_login_callback(sender, **kwargs):

    attributes = kwargs.get('attributes')
    user = kwargs.get('user')

    if attributes and user:

        roles = attributes.get('roles')

        if roles:
            user.groups.clear()
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
