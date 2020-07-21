from django import template
from django.utils.module_loading import import_string
from django.utils.translation import get_language

from rest_framework.renderers import HTMLFormRenderer

from djvue.defaults import VV_LOCALE_PATH

register = template.Library()


@register.simple_tag
def render_vue_field(field, style=None, template_pack="vue/default/"):
    style = {} if style is None else style
    if template_pack:
        style["template_pack"] = template_pack
    renderer = style.get("renderer", HTMLFormRenderer())
    return renderer.render_field(field, style)


@register.simple_tag
def render_vue_form(serializer, template_pack=None):
    style = {"template_pack": template_pack or "vue/default"}
    renderer = HTMLFormRenderer()
    return renderer.render(serializer.data, None, {"style": style})


@register.inclusion_tag("vue/starter.html")
def vue_starter():
    vv_locale = import_string(VV_LOCALE_PATH)
    lang = get_language()
    ret = {
        "vv_language": lang,
    }
    try:
        ret["vv_locale"] = vv_locale[lang]
    except KeyError:
        pass
    return ret
