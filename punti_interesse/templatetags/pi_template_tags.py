from django import template
from django.utils.html import escape

register = template.Library()

@register.filter
def is_rilevatore(user):
    return user.groups.filter(name='Rilevatore').exists()

@register.filter
def is_validatore(user):
    return user.groups.filter(name='Validatore').exists()

@register.inclusion_tag('punti_interesse/form_buttons.html', takes_context=True)
def form_buttons(context):
    return {'punto': context.get('punto', None)}

@register.inclusion_tag('top_scroll.html')
def btn_scroll_top():
    return {}

@register.filter
def markup(text):
    escaped = escape(text)
    return mark_italic(escaped)

def mark_italic(text):
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
