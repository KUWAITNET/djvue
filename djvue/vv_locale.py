# Parent key is matching the django language.
# Child key is matching the VeeValidate lang codes
# https://logaretm.github.io/vee-validate/guide/localization.html#using-the-default-i18n

vv_locale = {
    "ar": {
        "ar": {
            "messages": {
                "alpha": "{_field_} يجب ان يحتوي على حروف فقط",
                "alpha_num": "{_field_} قد يحتوي فقط على حروف وارقام",
                "alpha_dash": "{_field_} قد يحتوي على حروف او الرموز - و _",
                "alpha_spaces": "{_field_} قد يحتوي فقط على حروف ومسافات",
                "between": "قيمة {_field_} يجب ان تكون ما بين {min} و {max}",
                "confirmed": "{_field_} لا يماثل التأكيد",
                "digits": "{_field_} يجب ان تحتوي فقط على ارقام والا يزيد عددها عن {length} رقم",
                "dimensions": "{_field_} يجب ان تكون بمقاس {width} بكسل في {height} بكسل",
                "email": "{_field_} يجب ان يكون بريدا اليكتروني صحيح",
                "excluded": "الحقل {_field_} غير صحيح",
                "ext": "نوع ملف {_field_} غير صحيح",
                "image": "{_field_} يجب ان تكون صورة",
                "integer": "الحقل {_field_} يجب ان يكون عدداً صحيحاً",
                "length": "حقل {_field_} يجب الا يزيد عن {length}",
                "max_value": "قيمة الحقل {_field_} يجب ان تكون اصغر من {min} او تساويها",
                "max": "الحقل {_field_} يجب ان يحتوي على {length} حروف على الأكثر",
                "mimes": "نوع ملف {_field_} غير صحيح",
                "min_value": "قيمة الحقل {_field_} يجب ان تكون اكبر من {min} او تساويها",
                "min": "الحقل {_field_} يجب ان يحتوي على {length} حروف على الأقل",
                "numeric": "{_field_} يمكن ان يحتوي فقط على ارقام",
                "oneOf": "الحقل {_field_} يجب ان يكون قيمة صحيحة",
                "regex": "الحقل {_field_} غير صحيح",
                "required": "{_field_} مطلوب",
                "required_if": "حقل {_field_} مطلوب",
                "size": "{_field_} يجب ان يكون اقل من {size} كيلوبايت",
            }
        }
    },
    "en-us": {
        "en": {
            "messages": {
                "alpha": "The {_field_} field may only contain alphabetic characters",
                "alpha_num": "The {_field_} field may only contain alpha-numeric characters",
                "alpha_dash": "The {_field_} field may contain alpha-numeric characters as well as dashes and underscores",
                "alpha_spaces": "The {_field_} field may only contain alphabetic characters as well as spaces",
                "between": "The {_field_} field must be between {min} and {max}",
                "confirmed": "The {_field_} field confirmation does not match",
                "digits": "The {_field_} field must be numeric and exactly contain {length} digits",
                "dimensions": "The {_field_} field must be {width} pixels by {height} pixels",
                "email": "The {_field_} field must be a valid email",
                "excluded": "The {_field_} field is not a valid value",
                "ext": "The {_field_} field is not a valid file",
                "image": "The {_field_} field must be an image",
                "integer": "The {_field_} field must be an integer",
                "length": "The {_field_} field must be {length} long",
                "max_value": "The {_field_} field must be {max} or less",
                "max": "The {_field_} field may not be greater than {length} characters",
                "mimes": "The {_field_} field must have a valid file type",
                "min_value": "The {_field_} field must be {min} or more",
                "min": "The {_field_} field must be at least {length} characters",
                "numeric": "The {_field_} field may only contain numeric characters",
                "oneOf": "The {_field_} field is not a valid value",
                "regex": "The {_field_} field format is invalid",
                "required_if": "The {_field_} field is required",
                "required": "The {_field_} field is required",
                "size": "The {_field_} field size must be less than {size}KB",
            }
        }
    },
}
