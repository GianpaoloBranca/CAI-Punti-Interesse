from django import template

register = template.Library()

@register.filter
def is_rilevatore(user):
    return user.groups.filter(name='Rilevatore').exists()

@register.filter
def is_validatore(user):
    return user.groups.filter(name='Validatore').exists()

@register.inclusion_tag('top_scroll.html')
def btn_scroll_top():
    return {}