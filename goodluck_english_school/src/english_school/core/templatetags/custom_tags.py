from django import template

register = template.Library()


@register.filter(name='custom_pluralize', is_safe=True)
def custom_pluralize(age, forms):
    forms = forms.split(',')
    primary_remainder = abs(age) % 100
    secondary_remainder = primary_remainder % 10
    if 10 < secondary_remainder < 21:
        return forms[2]
    if 1 < secondary_remainder < 5:
        return forms[1]
    if secondary_remainder == 1:
        return forms[0]
    return forms[2]