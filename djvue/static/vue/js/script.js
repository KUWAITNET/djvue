let nonFieldErrorsKey = "non_field_errors"
let detailErrorKey = "detail"
let errorKeys = [nonFieldErrorsKey, detailErrorKey]

let djMixin = {
  delimiters: ["{(", ")}"],
  data() {
    return {
      options: {},
      nonFieldErrors: [],
      actionURL: null,
      form: {},
      formsetRefs: [],
    }
  },
  mounted() {
    axios.options(this.actionURL).then((response) => {
      this.options = response.data.actions.POST
    })
  },
  methods: {
    submit() {
      // reset errors
      this.nonFieldErrors = []
      axios.post(this.actionURL, this.form).then(this.success).catch(this.error)
    },
    success(response) {
      console.log(response)
    },
    error(error, ref = "form") {
      if (error.response) {
        let errors = error.response.data
        this.renderFieldErrors(errors, ref)
      } else {
        this.nonFieldErrors.push(error.message)
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
        // formset field errors //
        this.renderFormsetsError(errors)
        // form errors
        this.$refs[ref].setErrors(errors)
      }
    },

    renderFormsetsError(errors) {
      this.formsetRefs.forEach((formsetItem) => {
        if (errors.hasOwnProperty(formsetItem)) {
          let formsetErrors = errors[formsetItem]

          formsetErrors.forEach((item, index) => {
            Object.keys(item).map((key) => {
              if (!errorKeys.includes(key)) {
                item[`${key}-${index}`] = item[key]
                delete item[key]
              }
            })
            // console.log(formsetItem, item)
            this.$refs[formsetItem].setErrors(item)
            this.renderFieldErrors(item, formsetItem)
          })
        }
      })
    },
    uploadFile(event) {
      let formData = new FormData()
      // save vue instance for being able to refence it later.
      const vm = this
      // get the parent field name
      const parentFieldName = event.target.name.split(".")[0]

      formData.append("file", event.target.files[0])
      axios
        .post(this.fileUploadURL, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then(({data}) => {
          // save details on the form data which will be sent to the server
          vm.form[parentFieldName].filename = data.filename
          vm.form[parentFieldName].path = data.path
        })
        .catch((error) => this.error(error, parentFieldName))
    },
  },
}
