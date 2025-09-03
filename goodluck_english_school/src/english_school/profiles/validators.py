from datetime import date

from django.core.exceptions import ValidationError

from core.constants import (
    DAYS_IN_YEAR,
    MIN_VALID_AGE,
    MAX_VALID_AGE,
    ADULT_AVG_AGE,
)


def validate_age_range(value: date, min_age: int, max_age: int, error_msg: str) -> None:
    """Validate the age of the user against a given age range."""
    age = (date.today() - value).days // DAYS_IN_YEAR

    if age < min_age or age > max_age:
        raise ValidationError(error_msg)


def real_age(value: date) -> None:
    """Determine the reality of the user's age."""
    validate_age_range(
        value=value,
        min_age=MIN_VALID_AGE,
        max_age=MAX_VALID_AGE,
        error_msg=(
            f'Ожидается возраст от {MIN_VALID_AGE} до {MAX_VALID_AGE} лет'
        ),
    )

def is_teenager(value: date) -> None:
    """Determines the user's age of a teenager."""
    validate_age_range(
        value=value,
        min_age=ADULT_AVG_AGE,
        max_age=MAX_VALID_AGE,
        error_msg=(
            f'Необходимо достигнуть {ADULT_AVG_AGE}-летнего возраста!'
        )
    )