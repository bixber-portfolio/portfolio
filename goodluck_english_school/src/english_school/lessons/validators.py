from django.core.exceptions import ValidationError

def validate_time_interval(value):
    if value.minute % 30 != 0 or value.second != 0:
        raise ValidationError(
            'Выберите время, кратное 30 минутам'
        )