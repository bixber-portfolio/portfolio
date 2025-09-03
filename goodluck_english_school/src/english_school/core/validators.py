from django.core.exceptions import ValidationError

def starts_with_uppercase(value: str):
    first_simbol = value[0]
    if value and not first_simbol.isupper() and not first_simbol.isdigit():
        raise ValidationError('Поле должно начинаться с большой буквы.')
