import re
from datetime import datetime as dt

from django.core.exceptions import ValidationError


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError(
            'Недопустимое имя пользователя!'
        )
    if not bool(re.match(r'^[\w.@+-]+$', value)):
        raise ValidationError(
            'Некорректные символы в username'
        )
    return value


def current_year_validator(value):
    if value > dt.now().year:
        raise ValidationError(
            (f'{value} год ещё не наступил.'),
            params={'value': value},
        )
