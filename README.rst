=====
DjVue
=====

*Handle Django forms with Vue.js and Django REST Framework*


This project aims to help to build hybrid views that handle both templates renders as well as the REST API. Useful when the client doesn't have a SPA for the frontend but does need mobile apps or an API or developing an API in an existing project that is required. I suggest checking the ``example`` app for seeing a concrete implementation.

The trade-off made is getting rid of `Django Forms <https://docs.djangoproject.com/en/3.0/topics/forms/>`_ and replace them with `Django REST Framework form renderer. <https://www.django-rest-framework.org/topics/html-and-forms/#rendering-forms>`_

============
Requirements
============

* `Django <https://www.djangoproject.com/>`__ (2.2+)
* `DRF <https://www.django-rest-framework.org>`_

For the form validation and submission:

* `Vue.js 2.6 <https://vuejs.org/>`_
* `VeeValidate <https://logaretm.github.io/vee-validate/>`_


============
Installation
============

Install ``djvue`` (or `download from PyPI <http://pypi.python.org/pypi/djvue>`__):

.. code-block:: bash

    pip install djvue

Add ``djvue`` to ``INSTALLED_APPS`` in ``settings.py``:

.. code-block:: python

    INSTALLED_APPS = (
        # other apps
        "djvue",
    )

Enable session authentication for DRF.

.. warning::
    Failing in doing this will make all your views csrf exempted.


.. code-block:: python

    REST_FRAMEWORK = {
        # ...
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.SessionAuthentication',
            # ...
        ),
        # ...
    }


If there are files to be uploaded via forms, it's required to include ``djvue.urls`` in your root ``urls.py``:

.. code-block:: python

    # For Django >= 2.2
    urlpatterns += [
        path('', include('djvue.urls'))
    ]


============
How it works
============

***********************
Rendering a simple form
***********************


`DjVue` allows you to easily render straightforward forms.

Define the serializer.

.. code-block:: python

    class LoginSerializer(serializers.Serializer):
        email = serializers.EmailField(required=True)
        password = serializers.CharField(write_only=True, style={"input_type": "password"})


Your views will require to return the serializer definition and the rendered template on the GET requests, exactly like Django CBVs are doing.

.. code-block:: python

    from rest_framework.generics import CreateAPIView
    from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
    from rest_framework.response import Response

    from .serializers import LoginSerializer


    class LoginView(CreateAPIView):
        renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
        serializer_class = LoginSerializer
        template_name = "login.html"

        def get(self, request, *args, **kwargs):
            return Response({"serializer": self.get_serializer()})


Include the prerequisites at the bottom of ``base.html``

.. code-block:: HTML

     {% load vue_tags %}
     .... other scripts
     {% vue_starter %}


*******
Vue app
*******


Each form is another Vue instance.

.. code-block:: HTML

    <div id="login-app" hidden>
        ...
    </div>

.. note::
    Hide the div holding the Vue.js app to avoid showing to the user un-rendered HTML using the ``hidden`` HTML attribute. It can be removed once the DOM has loaded, placed usually at the end of the script.


***************
Form definition
***************

validation-observer
-------------------

Define the form using VeeValidates's `ValidationObserver <https://logaretm.github.io/vee-validate/api/validation-observer.html#scoped-slot-props>`_ component.

render_vue_form
---------------

Render the serializer as an HTML form using ``render_vue_form``. This template tag is a wrapper around the original DRF `render_form <https://www.django-rest-framework.org/topics/html-and-forms/#rendering-forms>`_ template tag which changes the field style.


.. code-block:: HTML

    <validation-observer ref="form" v-slot="{ handleSubmit }" mode="lazy">
        <form @submit.prevent="handleSubmit(submit)" novalidate="true">
            <div class="row">
                <div class="col-sm">
                    {% render_vue_form serializer %}
                </div>
            </div>
            <button class="btn btn-primary">Login</button>
        </form>
    </validation-observer>

render_vue_field
----------------

For a more granular control ``render_vue_field`` template tag can be used.


.. code-block:: HTML

    <validation-observer ref="form" v-slot="{ handleSubmit }" mode="lazy">
        <form @submit.prevent="handleSubmit(submit)" novalidate="true">
            <div class="row">
                <div class="col-sm">
                    {% render_vue_field serializer.username %}
                    {% render_vue_field serializer.password %}
                </div>
            </div>
            <button class="btn btn-primary">Login</button>
        </form>
    </validation-observer>


**********
djVueMixin
**********

* Create a new Vue app and use djVueMixin which handles the form validation, file upload, and submission.
* Define the form fields inside ``data`` method ``form`` object. Note that you need to define manually every form field that has to be passed to the server, excepting file fields, which will cover in another example later.

* **Mandatory implementation input**
    * **actionURL**: defines where the form has to be sent via a POST request to the server.
    * **success**: method is called when the server returns a success response (status 200).

.. code-block:: javascript


    new Vue({
        el: '#login-app',
        mixins: [djVueMixin],
        data() {
            return {
                actionURL: '{% url "login" %}',
                form: {
                    email: null,
                    password: null
                }
            }
        },
        methods: {
            success(response) {
                window.location.href = "{% url 'user:dashboard' %}"
            }
        }

    })
    // remove hidden
    let appEl = document.getElementById('login-app');
    appEl.removeAttribute("hidden");



*****************************
Display the validation errors
*****************************

* At this step, live validation is setup. Each form field is validated individually in the partial HTML field. It can be customized by creating a new `template pack <https://www.django-rest-framework.org/topics/html-and-forms/#using-template-packs>`_. Add a placeholder anywhere on the page for rendering forms global validation error like ``Server Error`` or better use a `toastr <https://github.com//s4l1h/vue-toastr>`_ or SnackBar.
* Displaying server side field errors is implemented only for one nesting level, if you need more you should override ``error`` method from ``djVueMixin``.

.. code-block:: HTML

    <p v-for="error in nonFieldErrors" :key="error" class="text-danger">{( error )}</p>


**************
Advanced usage
**************

.. code-block:: python

    from djvue.fields import FileField

    class WorkSerializer(serializers.Serializer):
        CHOICES = (
            ("cc", "Chocolate Tested"),
            ("dreamer", "Dreamer"),
            ("sp", "Smokes packing"),
        )
        job = serializers.ChoiceField(choices=CHOICES)
        position = serializers.CharField(required=False)


    class ProfileSerializer(serializers.ModelSerializer):
        username = serializers.CharField(max_length=25, min_length=3, required=True,)
        email = serializers.EmailField(required=True)
        password1 = serializers.CharField(
            write_only=True,
            style={"input_type": "password", "rules": "password:@password2"},
        )
        password2 = serializers.CharField(write_only=True, style={"input_type": "password"})
        file = FileField(required=True)
        working_place = WorkSerializer(write_only=True)

        class Meta:
            model = Profile
            fields = (
                "username",
                "email",
                "password1",
                "password2",
                "file",
                "working_place",
            )


File upload
-----------

* File upload starts as soon as ``onchange`` DOM event occurs. Behind the scene, a global view is uploading the file to a temporary location and returns to the client the ``path`` and the original ``filename`` which will be sent together with the form data upon submission. If you want to enforce special validation, DjVue batteries can be subclasses to create your custom logic.
* To enable file upload, it's required to use DjVue's ``FileField`` instead of the default one.

FileField
^^^^^^^^^

A hybrid file field. Renders an input type, accepts as input a dictionary containing the filename and the file path and it serializes the representation like a native serializer.FileField.

``serializers.py``

.. code-block:: python

    from django.core.validators import FileExtensionValidator

    from djvue.serializers import FileUploadSerializer


    class PDFUploadSerializer(FileUploadSerializer):
        """
        Allows only PDF files to be uploaded
        """
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["file"].validators.append(FileExtensionValidator(allowed_extensions=['pdf']))

``views.py``

.. code-block:: python

    from djvue.views import FileUploadView

    class PDFUploadView(FileUploadView):
        serializer_class = PDFUploadSerializer

``urls.py``

.. code-block:: python

        urlpatterns = [
            path('<scrambled-url>', PDFUploadView.as_view(), name="pdf_upload")
           ]


Once the backend is implemented, the Vue.js app is left to be updated and that's all.

.. code-block:: javascript

    new Vue({
        // ...
        uploadURL: "{% url 'pdf_upload' %}"
        // ...
    })


Upon form submission, the uploaded files must be linked with some model or pushed somewhere else. Let's see a trivial example of how that can be done, ``filename`` and ``path`` are always returned by the view using ``FileUploadSerializer`` and ``djVueMixin`` does the job of POSTing them to the ``actionURL`` together with the rest of the form fields.

The current example considers one url for all files which belong to the same form, for handling different validations per file, each field can have it's own upload url by defining ``upload_url`` in field style.

.. code-block:: python

    pdf = FileField(style={"upload_url": reverse_lazy("pdf_upload")})
    image = FileField(style={"upload_url": reverse_lazy("image_upload")})

``serializers.py``

.. code-block:: python

    class ProfileSerializer(serializers.ModelSerializer):
        def create(self, validated_data):
            user_file = validated_data.pop("file", None)
            profile = Profile.objects.create(**validated_data)
            # # fetch the file from temporary dir
            if user_file is not None and all(
                [user_file.get("path", False), user_file.get("filename", False)]
            ):
                with open(user_file["path"], "rb") as f:
                    profile.file.save(user_file["filename"], f)
            return profile



Fieldsets
---------

By default, DjVue can handle also nested serializers with one nesting level, though if you need more, this behavior can be easily changed. Child serializer fields will be rendered in the same format that parent fields are. The only adjustment required to support them is to modify the ``form`` key from the ``data`` method to include an object which defines the child serializer fields rather than a key-value pair.

.. code-block:: javascript

    new Vue({
        // ...
        data() {
            return {
                form: {
                    // ...
                    working_place: {
                        job: null,
                        position: null
                    }
                }
            }
    },

        // ...
    })


Formsets
--------

At this moment formset are indeed supported, but they have to be written by hand. It's on the road map to provide utilities for them also. Here's a naive implementation of how they can be done:

``serializers.py``

.. code-block:: python

    class AddressSerializer(serializers.Serializer):
        COUNTRY_CHOICES = (("ro", "Romania"), ("de", "Germany"), ("kw", "Kuwait"))
        country = serializers.ChoiceField(choices=COUNTRY_CHOICES)
        zip_code = serializers.CharField()
        address = serializers.CharField(required=False)

        class Meta:
            list_serializer_class = serializers.ListSerializer


    class ProfileSerializer(serializers.ModelSerializer):
        # ...
        addresses = AddressSerializer(many=True)

``script.js``

.. code-block:: javascript

        let addressIndex = 0

        new Vue({
            // ..
            data() {
                return {
                    formsetReady: false,
                    formsetDefinition: {},
                    form: {
                        // ..
                        addresses: [
                            {
                                id: `address-${addressIndex}`,
                                country: null,
                                zip_code: null,
                                address: null
                            }
                        ]
                    },
                }
            },
            watch: {
                options() {
                    // set the formset definitions
                    this.formsetDefinition = this.options.addresses.child.children
                    this.formsetReady = true
                }
            },
            methods: {
                addAddress() {
                    addressIndex++
                    this.form.addresses.push({
                        id: `address-${addressIndex}`,
                        country: null,
                        zip_code: null,
                        address: null,
                    })
                },
                deleteAddress(index) {
                    this.form.addresses.splice(index, 1)
                },

            }
        })

Place the formset anywhere inside the form definition wrapped with its own ``validation-observer``.

``index.html``

.. code-block:: HTML

    <validation-observer ref="addresses">
        <div class="card mb-3" v-for="(address, index) in form.addresses" :key="address.id">
            <div class="card-body">
                <span class="float-right" style="cursor: pointer"
                      @click="deleteAddress(index)">x</span>
                <h4 class="card-title">Address</h4>
                <div class="address-form">

                    <validation-provider :name="`country-${index}`" rules="required"
                                         v-slot="{ errors, valid, invalid, validated }" tag="div"
                                         class="form-group">
                        <select v-model="address.country"
                                class="form-control"
                                name="country"
                                :class="{'is-invalid': validated && invalid, 'is-valid': valid}"
                        >
                            <option disabled value="">Select country</option>

                            <option v-for="opt in formsetDefinition.country.choices"
                                    :value="opt.value">
                                {( opt.display_name )}
                            </option>

                        </select>
                        <p v-for="error in errors" :key="error" class="text-danger">{( error )}</p>
                    </validation-provider>

                    <validation-provider :name="`zip_code-${index}`" rules="required"
                                         v-slot="{ errors, valid, invalid, validated }" tag="div"
                                         class="form-group">
                        <input v-model="address.zip_code"
                               type="text"
                               class="form-control mb-2"
                               :class="{'is-invalid': validated && invalid, 'is-valid': valid}"
                               placeholder="Zip Code">
                        <p v-for="error in errors" :key="error" class="text-danger">{( error )}</p>
                    </validation-provider>

                    <validation-provider :name="`address-${index}`" rules="required"
                                         v-slot="{ errors, valid, invalid, validated }" tag="div"
                                         class="form-group">
                        <textarea v-model="address.address"
                                  type="text"
                                  class="form-control mb-2"
                                  :class="{'is-invalid': validated && invalid, 'is-valid': valid}"
                                  placeholder="Address"></textarea>
                        <p v-for="error in errors" :key="error" class="text-danger">{( error )}</p>
                    </validation-provider>

                </div>
            </div>
        </div>
    </validation-observer>


i18n and custom field error messages
------------------------------------

By default, error messages are rendered in the English language. In order to change them, add in ``settings.py`` the path of the file where new messages are located.

``settings.py``

.. code-block:: python

    LANGUAGE_CODE = "en-us"

    DJVUE_VV_LOCALE_PATH = "example.locale.djvue_messages"

This file must contain a dictionary that matches the language codes defined in  `LANGUAGES <https://docs.djangoproject.com/en/3.0/ref/settings/#languages>`_ or if your project is not multilingual and if you need to override the default messages, define a dictionary with one key which is matching `LANGUAGE_CODE <https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-LANGUAGE_CODE>`_ value. The children key which holds the messages must match the `VeeValidate keys  <https://github.com/logaretm/vee-validate/tree/master/locale>`_.

``djvue_messages.py``

.. code-block:: python

    vv_locale = {
        "en-us": {
            "en": {
                "messages": {
                    "alpha": "This field may only contain alphabetic characters.",
                }
            }
        },
    }


=====
TODOs
=====

* Generate form object from the serializer definition.
* Provide utilities for dynamic formsets.
* Handle unlimited levels of nested serializers?

=======
Credits
=======


Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackagetoin
