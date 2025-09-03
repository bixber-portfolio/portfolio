from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from django.core.validators import BaseValidator

BAD_WORDS = []

SYMBOLS_DATA = {'а' : ['а', 'a', '@'],
  'б' : ['б', '6', 'b'],
  'в' : ['в', 'b', 'v'],
  'г' : ['г', 'r', 'g'],
  'д' : ['д', 'd'],
  'е' : ['е', 'e'],
  'ё' : ['ё', 'e'],
  'ж' : ['ж', 'zh', '*'],
  'з' : ['з', '3', 'z'],
  'и' : ['и', 'u', 'i'],
  'й' : ['й', 'u', 'i'],
  'к' : ['к', 'k', 'i{', '|{'],
  'л' : ['л', 'l', 'ji'],
  'м' : ['м', 'm'],
  'н' : ['н', 'h', 'n'],
  'о' : ['о', 'o', '0'],
  'п' : ['п', 'n', 'p'],
  'р' : ['р', 'r', 'p'],
  'с' : ['с', 'c', 's'],
  'т' : ['т', 'm', 't'],
  'у' : ['у', 'y', 'u'],
  'ф' : ['ф', 'f'],
  'х' : ['х', 'x', 'h' , '}{'],
  'ц' : ['ц', 'c', 'u,'],
  'ч' : ['ч', 'ch'],
  'ш' : ['ш', 'sh'],
  'щ' : ['щ', 'sch'],
  'ь' : ['ь', 'b'],
  'ы' : ['ы', 'bi'],
  'ъ' : ['ъ'],
  'э' : ['э', 'e'],
  'ю' : ['ю', 'io'],
  'я' : ['я', 'ya'],
}


class CensoreshipValidator(BaseValidator):
    '''Filter out bad words'''
    def __init__(self, text: str, message=None):
        self.text = text.lower().replace(" ", "")
        if message:
            self.message = message
    
    def __call__(self, text):
        cleaned = self.clean(text)
        item = self.find_bad_word(cleaned)
        if item:
            fragment, word = item
            raise ValidationError(
                f"Найдено нецензурное слово: '{fragment}'. Похоже на '{word}'"
            )

    def distance(self, a, b): 
        "Calculates the Levenshtein distance between a and b."
        n, m = len(a), len(b)
        if n > m:
            a, b = b, a
            n, m = m, n

        current_row = range(n + 1)
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
                if a[j - 1] != b[i - 1]:
                    change += 1
                current_row[j] = min(add, delete, change)

        return current_row[n]

    def find_bad_word(self, word):
        for key, value in SYMBOLS_DATA.items():
            for letter in value:
                for phr in self.text:
                    if letter == phr:
                        text = self.text.replace(phr, key)

        for word in BAD_WORDS:
            for part in range(len(text)):
                fragment = text[part: part+len(word)]
                if self.distance(fragment, word) <= len(word)*0.25:
                    return (fragment, word)

phone_validator = RegexValidator(
    regex=r'^(8|\+7)\d{10}$',
    message="Номер телефона должен быть в формате +7XXXXXXXXXX или 8XXXXXXXXXX",
    code='invalid_phone'
)