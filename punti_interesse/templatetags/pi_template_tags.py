from django import template
from django.utils.html import escape

register = template.Library()

@register.filter
def is_rilevatore(user):
    return user.groups.filter(name='Rilevatore').exists()

@register.filter
def is_validatore(user):
    return user.groups.filter(name='Validatore').exists()

@register.filter
def markup(text):
    escaped = escape(text)
    return _mark_italic(escaped)

def _mark_italic(text):
    output = ''
    split_t = text.split('**')

    in_i = False
    counter = 0
    last = len(split_t) - 1

    for elem in split_t:
        if in_i:
            # this means we have an odd number of '**'. Ignores the last one.
            if counter == last:
                output += '**' + elem
            else:
                output += '<i>' + elem + '</i>'
                in_i = False
        else:
            output += elem
            in_i = True
        counter += 1
    return output
