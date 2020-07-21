from django import template

from rest_framework.renderers import HTMLFormRenderer
from ..v_locale import en, ar

register = template.Library()


@register.simple_tag
def render_vue_field(field, style=None, template_pack='vue/default/', **kwargs):
    style = {} if style is None else style
    if template_pack:
        style['template_pack'] = template_pack
    style.update(kwargs)
    renderer = style.get('renderer', HTMLFormRenderer())
    return renderer.render_field(field, style)


@register.simple_tag
def render_vue_form(serializer, template_pack=None):
    style = {'template_pack': template_pack or 'vue/default'}
    renderer = HTMLFormRenderer()
    return renderer.render(serializer.data, None, {'style': style})


@register.inclusion_tag('vue/starter.html', takes_context=True)
def vue_starter(context):
    request = context['request']
    return {
        'vee_validate_locale': ar if request.LANGUAGE_CODE == 'ar' else en,
    }
