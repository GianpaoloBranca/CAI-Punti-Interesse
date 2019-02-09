from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.utils.translation import ugettext as _


def validate_degree(value):
    if value > 180.0 or value < -180.0:
        raise ValidationError("Assicurati che il valore sia compreso tra -180 e 180")

class MaxSizeValidator(MaxValueValidator):
    message = _('Il file eccede la dimensione massima di %(limit_value)s MB.')

    def __call__(self, value):
        # get the file size as cleaned value
        cleaned = self.clean(value.size)
        params = {'limit_value': self.limit_value, 'show_value': cleaned, 'value': value}
        if self.compare(cleaned, self.limit_value * 1024 * 1024): # convert limit_value from MB to Bytes
            raise ValidationError(self.message, code=self.code, params=params)
