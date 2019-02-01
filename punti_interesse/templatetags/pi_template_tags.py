from django import template

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
