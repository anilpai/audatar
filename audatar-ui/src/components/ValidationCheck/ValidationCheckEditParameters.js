import React from 'react'
import PropTypes from 'prop-types'
import SelectInput from '../Input/SelectInput'
import TextInput from '../Input/TextInput'
import TextAreaInput from '../Input/TextAreaInput'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import { getValidator } from '../../actions/validator'

class ValidationCheckEditParameters extends React.Component {
  renderParameter = (parameter, i) => {
    switch (parameter.type) {
      case 'SelectField':
      case 'ConnectionField':
        return (
          <SelectInput
            key={i}
            label={parameter.label}
            tooltip={parameter.description}
            options={parameter.options}
            allowMultiple={parameter.allow_multiple}
            model={`validationcheckform.parameters[${i}].parameter_value`}
            disabled={this.props.isSaving}
          />
        )
      case 'TextField':
        return (
          <TextInput
            key={i}
            label={parameter.label}
            tooltip={parameter.description}
            model={`validationcheckform.parameters[${i}].parameter_value`}
            disabled={this.props.isSaving}
            valid={
              this.props.form.parameters[i] &&
              (this.props.form.parameters[i].parameter_value.pristine ||
                this.props.form.parameters[i].parameter_value.valid)
            }
          />
        )
      case 'TextAreaField':
        return (
          <TextAreaInput
            key={i}
            label={parameter.label}
            rows={parameter.rows}
            placeholder={parameter.placeholder}
            tooltip={parameter.description}
            model={`validationcheckform.parameters[${i}].parameter_value`}
            disabled={this.props.isSaving}
            valid={
              this.props.form.parameters[i] &&
              (this.props.form.parameters[i].parameter_value.pristine ||
                this.props.form.parameters[i].parameter_value.valid)
            }
          />
        )
      default:
        throw new Error(`Unknown field type: ${parameter.type}`)
    }
  }

  render() {
    return (
      <div>
        {this.props.parameters &&
          this.props.parameters.map((parameter, i) => {
            return this.renderParameter(parameter, i)
          })}
      </div>
    )
  }
}

ValidationCheckEditParameters.propTypes = {
  parameters: PropTypes.array,
  disabled: PropTypes.bool
}

const mapStateToProps = state => {
  return {
    validator: state.validator,
    isSaving: state.validationcheck.save.isSaving,
    form: state.forms.validationcheckform
  }
}

const mapDispatchToProps = dispatch => {
  return bindActionCreators({ getValidator }, dispatch)
}

export default connect(mapStateToProps, mapDispatchToProps)(
  ValidationCheckEditParameters
)
