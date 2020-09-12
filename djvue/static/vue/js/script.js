let nonFieldErrorsKey = "non_field_errors"
let detailErrorKey = "detail"
let errorKeys = [nonFieldErrorsKey, detailErrorKey]

let djVueMixin = {
  delimiters: ["{(", ")}"],
  data() {
    return {
      options: {},
      nonFieldErrors: [],
      actionURL: null,
      form: {},
      files: {},
      fileUploadURL: uploadURL
    }
  },
  mounted() {
    axios.options(this.actionURL).then((response) => {
      this.options = response.data.actions.POST
    })
  },
  methods: {
    getFieldsetRefs() {
      return Object.keys(this.form).filter(key => _.isPlainObject(this.form[key]))
    },
    getFormsetRefs() {
      return Object.keys(this.form).filter(key => _.isArray(this.form[key]))
    },
    submit() {
      // reset errors
      this.nonFieldErrors = []
      axios.post(this.actionURL, Object.assign({}, this.form, this.files))
          .then(this.success)
          .catch(this.error)
    },
    success(response) {
      alert("You must implemented success method.")
    },
    error(error, ref = "form") {

      if (error.response && error.response.status === 400) {
        let errors = error.response.data
        this.renderFieldErrors(errors, ref)
      } else {
        this.nonFieldErrors.push("Error! Contact an administrator.")
      }
    },
    renderFieldErrors(errors, ref = "form") {
      if (_.has(errors, "detail")) {
        // rest framework _detail_ error: IE: object not found
        this.nonFieldErrors.push(errors["detail"])
      } else if (_.has(errors, nonFieldErrorsKey)) {
        // rest framework _non_field_errors_: global error
        this.nonFieldErrors = errors[nonFieldErrorsKey]
      } else if (!_.has(errors, nonFieldErrorsKey)) {
        // fieldset errors
        this.renderFieldsetErrors(errors)
        // formset errors
        this.renderFormsetErrors(errors)

        // field errors
        // remove all keys that are having . or values are {}
        // to avoid double rendering of nested errors
        let fieldErrors = {}

        Object.keys(errors).forEach(key=> {
          if (!key.includes('.') && _.isArray(errors[key])) fieldErrors[key] = errors[key]
        })

        this.$refs[ref].setErrors(fieldErrors)
      }
    },

    renderFieldsetErrors(errors) {
      this.getFieldsetRefs().forEach(fieldsetRef => {
        if (errors.hasOwnProperty(fieldsetRef)) {
          // append the parent name to the field name
          let fieldsetErrors = errors[fieldsetRef]
          Object.keys(fieldsetErrors).forEach(key => {
            if (!errorKeys.includes(key)) {
              fieldsetErrors[`${fieldsetRef}.${key}`] = fieldsetErrors[key]
              delete fieldsetErrors[key]
            }
          })

          // raise field errors
          this.$refs[fieldsetRef].setErrors(fieldsetErrors)
          // raise global errors like non_field_errors
          this.renderFieldErrors(fieldsetErrors, fieldsetRef)
        }
      })
    },

    renderFormsetErrors(errors) {
      this.getFormsetRefs().forEach(formsetItem => {
        // if errors[formsetItem] is object, means
        // the error is fieldset related and not for
        // the formsets, so skip it quickly
        if (errors.hasOwnProperty(formsetItem)) {
          let formsetErrors = errors[formsetItem]

          // append index to each field name
          formsetErrors.forEach((item, index) => {
            Object.keys(item).map((key) => {
              if (!errorKeys.includes(key)) {
                item[`${key}-${index}`] = item[key]
                delete item[key]
              }
            })
            this.$refs[formsetItem].setErrors(item)
            this.renderFieldErrors(item, formsetItem)
          })
        }
      })
    },
    uploadFile(event, url) {
      let formData = new FormData()
      // save vue instance for being able to reference it later.
      const vm = this
      // clear the errors
      this.$refs.form.setErrors({[event.target.name]: []})

      let uploadURL = url !== "" ? url: this.fileUploadURL

      formData.append("file", event.target.files[0])
      axios
        .post(uploadURL, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then(({ data }) => {
          // save details on the form data which will be sent to the server
          Vue.set(vm.files, event.target.name, data)
        })
        .catch((error) => {
          // remove the file from the input
          event.target.value = null
          vm.error(error)
        })
    },
  },
}
