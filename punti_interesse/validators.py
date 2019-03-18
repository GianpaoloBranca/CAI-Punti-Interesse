from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from punti_interesse.templatetags.pi_template_tags import is_rilevatore, is_validatore

def validate_degree(value):
    if value > 180.0 or value < -180.0:
        raise ValidationError("Assicurati che il valore sia compreso tra -180 e 180")

def validate_punto_rilevatore(uid):
    user = User.objects.get(id=uid)
    if not is_rilevatore(user) and not user.is_superuser:
        raise ValidationError("Questo utente non può essere impostato come il rilevatore del punto di interesse")

class MaxSizeValidator(MaxValueValidator):
    message = _('Il file eccede la dimensione massima di %(limit_value)s MB.')

    def __call__(self, value):
        # get the file size as cleaned value
        cleaned = self.clean(value.size)
        params = {'limit_value': self.limit_value, 'show_value': cleaned, 'value': value}
        if self.compare(cleaned, self.limit_value * 1024 * 1024): # convert limit_value from MB to Bytes
            raise ValidationError(self.message, code=self.code, params=params)
