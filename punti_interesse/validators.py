from django.core.exceptions import ValidationError

def validate_degree(value):
    if value > 180.0 or value < -180.0:
        raise ValidationError("Assicurati che il valore sia compreso tra -180 e 180")
