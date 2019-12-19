import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { fetchValidators } from '../../actions/lookup'
import { getValidator } from '../../actions/validator'
import { Control, actions } from 'react-redux-form'

function ErrorMessage(props) {
  if ((props.teams || {}).errMsg) {
    return (
      <span className="help-block">
        Unable to load validators. Error: {props.validators.errMsg}
      </span>
    )
  } else {
    return null
  }
}

class ValidatorInput extends React.Component {
  componentDidMount() {
    this.props.fetchValidators().then(data => {
      if (this.props.model) {
        this.props.idChange(
          this.props.model,
          this.props.includeAllOption ? 0 : data[0].id
        )
        this.validatorChange(this.props.includeAllOption ? 0 : data[0].id)
      }
    })
  }

  handleChange = event => {
    this.validatorChange(event.target.value)
  }

  validatorChange = validatorId => {
    this.props.getValidator(validatorId).then(validator => {
      if (this.props.onChange) {
        this.props.onChange(validator)
      }
    })
  }

  render() {
    return (
      <div
        className={
          'form-group row ' +
          (this.props.validators && this.props.validators.errMsg
            ? 'has-error'
            : '')
        }
      >
        <label
          htmlFor={this.props.name}
          className="col-sm-2 col-form-label control-label"
        >
          {this.props.label || 'Validator'}
        </label>
        <div className="col-sm-10">
          <Control.select
            model={this.props.model || ' '}
            id={this.props.name}
            name={this.props.name}
            onChange={this.handleChange}
            className="form-control"
            disabled={this.props.disabled}
          >
            {this.props.includeAllOption && (
              <option value="0">All validators</option>
            )}
            {(this.props.validators || {}).data &&
              this.props.validators.data.map(item => {
                return (
                  <option key={item.id} value={item.id}>
                    {' '}
                    {item.name}{' '}
                  </option>
                )
              })}
          </Control.select>
          <ErrorMessage teams={this.props.validators} />
        </div>
      </div>
    )
  }
}

ValidatorInput.propTypes = {
  model: PropTypes.string,
  name: PropTypes.string,
  label: PropTypes.string,
  disabled: PropTypes.bool,
  onChange: PropTypes.func,
  includeAllOption: PropTypes.bool
}

const mapStateToProps = state => {
  return { validators: state.lookup.validators }
}

const mapDispatchToProps = dispatch => {
  return bindActionCreators(
    {
      fetchValidators,
      getValidator,
      idChange: (model, id) => actions.change(model, id)
    },
    dispatch
  )
}

export default connect(mapStateToProps, mapDispatchToProps)(ValidatorInput)
