from django.conf import settings


def _get(key, default):
    return getattr(settings, key, default)


VV_LOCALE_PATH = _get("DJVUE_VV_LOCALE_PATH", "djvue.vv_locale.vv_locale")
