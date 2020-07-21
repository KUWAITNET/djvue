from django.utils.translation import ugettext as _

from rest_framework.exceptions import ValidationError


class RequiredFileValidator:
    requires_context = True

    def __call__(self, value, serializer_field):
        if serializer_field.required and not all(list(value.values())):
            raise ValidationError(_("This field is required."))
