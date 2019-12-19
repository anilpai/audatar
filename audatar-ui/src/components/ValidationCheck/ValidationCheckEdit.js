import React from 'react'
import BasePage from '../BasePage'
import TeamInput from '../Input/TeamInput'
import DimensionInput from '../Input/DimensionInput'
import SeverityLevelInput from '../Input/SeverityLevelInput'
import TextInput from '../Input/TextInput'
import TextAreaInput from '../Input/TextAreaInput'
import ValidatorInput from '../Input/ValidatorInput'
import DatasetInput from '../Input/DatasetInput'
import TagInput from '../Input/TagInput'
import ValidationCheckEditNotifications from './ValidationCheckEditNotifications'
import ValidationCheckEditParameters from './ValidationCheckEditParameters'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import {
  getValidationCheck,
  saveValidationCheck
} from '../../actions/validationcheck'
import { Control, Form, Errors, actions } from 'react-redux-form'
import { LoadingOverlay } from '@homeaway/react-loading-overlay'
import { getValidator } from '../../actions/validator'
import log from '../../utils/AppLogger'

class ValidationCheckEdit extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      parameters: [],
      originalValidationCheck: {}
    }
    this.handleSubmit = this.handleSubmit.bind(this)
    this.validatorChange = this.validatorChange.bind(this)
    this.datasetSelect = this.datasetSelect.bind(this)
    this.tagChange = this.tagChange.bind(this)
    this.props.dispatch(actions.reset('validationcheckform'))
  }

  handleSubmit(validationCheck) {
    log.debug('Submitted validation check', validationCheck)

    // Mark the form as dirty once the user submits to show validation errors
    this.props.dispatch(actions.setDirty('validationcheckform'))

    // Submit if the form is valid
    if (this.props.form.$form.valid) {
      this.props.saveValidationCheck(validationCheck)
    }
  }

  componentDidMount() {
    if (this.props.match.params.id > 0) {
      this.props
        .getValidationCheck(this.props.match.params.id)
        .then(validationCheck => {
          this.setState({ originalValidationCheck: validationCheck })
          this.props
            .getValidator(validationCheck.validator_id)
            .then(validator => {
              this.validatorChange(validator)
            })
        })
    }
  }

  datasetSelect(dataset_uuid) {
    log.debug('Setting DataSet UUID', dataset_uuid)

    var validationCheck = Object.assign({}, this.props.validationCheck)
    validationCheck.dataset_id = dataset_uuid

    this.props.dispatch(
      actions.change(
        'validationcheckform.dataset_id',
        validationCheck.dataset_id
      )
    )

  }

  tagChange(tags){
    log.debug('Updating tags', tags)

    var validationCheck = Object.assign({}, this.props.validationCheck)
    validationCheck.tags = tags

    this.props.dispatch(
      actions.change(
        'validationcheckform.tags',
        validationCheck.tags
      )
    )

  }

  validatorChange(validator) {
    log.debug('Changed validator', validator)

    // Populate the validation check parameters with the validator fields
    var parameters = []
    var originalValidationCheckParameters =
      (this.state.originalValidationCheck || {}).parameters || []
    var existingValidationCheckParameters =
      (this.props.validationCheck || {}).parameters || []
    var validationCheck = Object.assign({}, this.props.validationCheck)

    validationCheck.validator_id = validator.id
    validationCheck.parameters = []

    validator.fields.forEach(field => {
      var originalParameter = originalValidationCheckParameters.find(function(
        parameter
      ) {
        return parameter.parameter_name === field.parameter_name
      })

      var existingParameter = existingValidationCheckParameters.find(function(
        parameter
      ) {
        return parameter.parameter_name === field.parameter_name
      })

      // Set parameter value to existing value, original value, default value, first option, or nothing (in that order)
      var parameterValue = ''
      if (existingParameter && existingParameter.parameter_value) {
        parameterValue = existingParameter.parameter_value
      } else if (originalParameter && originalParameter.parameter_value) {
        parameterValue = originalParameter.parameter_value
      } else if (field.default_value) {
        parameterValue = field.default_value
      } else if (field.options) {
        parameterValue = field.options[0].value
      }

      // Add parameter to validation check object
      validationCheck.parameters.push({
        id: existingParameter ? existingParameter.id : undefined,
        parameter_name: field.parameter_name,
        parameter_value: parameterValue
      })

      // Add parameter for display
      parameters.push({
        type: field.type,
        parameter_name: field.parameter_name,
        label: field.label,
        description: field.description,
        options: field.options,
        allow_multiple: field.allow_multiple,
        rows: field.rows,
        placeholder: field.placeholder
      })
    })

    this.props.dispatch(
      actions.change(
        'validationcheckform.parameters',
        validationCheck.parameters
      )
    )
    this.setState({ parameters })

    // Reset "touched" property so that validation isn't triggered again until after it's touched
    for (var i = 0; i < validationCheck.parameters.length; i++) {
      this.props.dispatch(
        actions.setPristine(
          `validationcheckform.parameters[${i}].parameter_value`
        )
      )
    }
  }

  render() {
    let url = process.env.REACT_APP_BASE_API_URL
    if (url === 'http://localhost:8080/api'){
      url = 'https://dataexplorer.homeawaycorp.com'
    } else if (url === 'https://audatar-api-dev.homeawaycorp.com/api'){
      url = 'http://data-discovery-prototype-test.eu-west-1-vpc-ddc17fb9.slb-internal.test.aws.away.black'
    }else if(url === 'https://audatar-api-stage.homeawaycorp.com/api'){
      url = 'http://data-discovery-prototype-stage.us-east-1-vpc-35196a52.slb-internal.stage.aws.away.black'
    }else {
      url = 'https://dataexplorer.homeawaycorp.com'
    }

    return (
      <BasePage
        title={
          this.props.match.params.id > 0
            ? 'Edit Validation Check'
            : 'Add Validation Check'
        }
      >
        <Form
          model="validationcheckform"
          onSubmit={validationcheck => this.handleSubmit(validationcheck)}
          noValidate
        >
          <Control type="hidden" model="validationcheckform.id" />

          <TextInput
            model="validationcheckform.name"
            label="Name"
            required
            disabled={this.props.isSaving}
            maxLength={128}
            valid={this.props.form.name.pristine || this.props.form.name.valid}
          />
          <TextAreaInput
            model="validationcheckform.description"
            label="Description"
            rows={3}
            required
            disabled={this.props.isSaving}
            maxLength={2000}
            valid={
              this.props.form.description.pristine ||
              this.props.form.description.valid
            }
          />

        <TagInput
            model="validationcheckform.tags"
            label="Tags"
            onChange={this.tagChange}
            disabled={this.props.isSaving}
          />
          <TeamInput
            model="validationcheckform.team_id"
            label="Portfolio"
            disabled={this.props.isSaving}
            setIdOnMount={this.props.validationCheck.id === 0}
          />
          <DatasetInput
            model="validationcheckform.dataset_name"
            label="Search Datasets"
            onSelect={this.datasetSelect}
            required
          />
          <TextInput
            model="validationcheckform.dataset_id"
            label="Dataset UUID"
            required
            disabled
            maxLength={36}
            tooltip={<a href={url+"/?query="+this.props.form.dataset_id.value+"&showall=true"}>Visit Data Explorer</a>}
            valid={
              this.props.form.dataset_id.pristine ||
              this.props.form.dataset_id.valid
            }
          />
          <SeverityLevelInput
            model="validationcheckform.severity_level_id"
            label="Severity"
            disabled={this.props.isSaving}
          />
          <DimensionInput
            model="validationcheckform.dimension_id"
            label="Dimension"
            disabled={this.props.isSaving}
          />
          <TextInput
            model="validationcheckform.documentation_url"
            label="Documentation URL"
            disabled={this.props.isSaving}
            maxLength={256}
          />
          {/* <CheckboxInput model="validationcheckform.is_active" label="Active" disabled={this.props.isSaving} /> */}
          <ValidatorInput
            model="validationcheckform.validator_id"
            label="Validator"
            onChange={this.validatorChange}
            disabled={this.props.isSaving}
          />
          <ValidationCheckEditParameters parameters={this.state.parameters} />
          <ValidationCheckEditNotifications
            notifications={this.props.validationCheck.notifications}
          />

          <div className="form-group row">
            <div className="col-sm-offset-2 col-sm-10">
              <input
                type="submit"
                value={this.props.isSaving ? 'Saving...' : 'Save'}
                className="btn btn-primary"
                disabled={this.props.isSaving}
              />
            </div>
          </div>

          <div className="form-group row">
            <div className="col-sm-offset-2 col-sm-10">
              {this.props.msg && (
                <div
                  className={
                    'alert ' +
                    (this.props.isError ? 'alert-danger' : 'alert-success')
                  }
                >
                  {' '}
                  {this.props.msg}
                </div>
              )}
              <Errors model="validationcheckform.parameters" />
            </div>
          </div>

          <LoadingOverlay loading={this.props.isFetching} />
        </Form>
      </BasePage>
    )
  }
}

const mapStateToProps = state => {
  return {
    data: state.validationcheck.save.data,
    msg: state.validationcheck.save.msg,
    isError: state.validationcheck.save.isError,
    isSaving: state.validationcheck.save.isSaving,
    validationCheck: state.validationcheckform,
    form: state.forms.validationcheckform,
    isFetching: state.validationcheck.fetch.isFetching
  }
}

const mapDispatchToProps = dispatch => {
  return bindActionCreators(
    { getValidationCheck, saveValidationCheck, getValidator },
    dispatch
  )
}

export default connect(mapStateToProps, mapDispatchToProps)(ValidationCheckEdit)
