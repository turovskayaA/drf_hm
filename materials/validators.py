import re

from rest_framework.exceptions import ValidationError


class UrlValidator:
    """
    Проверка на отсутствие в материалах ссылок на сторонние ресурсы, кроме youtube.com
    """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile('^https://www.youtube.com/')
        tmp = dict(value).get(self.field)
        if not bool(reg.match(tmp)):
            raise ValidationError('Ссылка должна быть только на Youtube, либо отсутствовать.')
