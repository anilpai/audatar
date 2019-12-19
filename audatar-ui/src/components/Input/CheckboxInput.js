import React from 'react'
import PropTypes from 'prop-types'
import { Control } from 'react-redux-form'

class CheckboxInput extends React.Component {
  handleChange = event => {
    if (this.props.onChange) {
      this.props.onChange(event)
    }
  }

  handleKeyDown = event => {
    if (this.props.onChange) {
      this.props.onKeyDown(event)
    }
  }

  render() {
    return (
      <div className="form-group row">
        <label
          htmlFor={this.props.name}
          className="col-sm-2 col-form-label control-label"
          title={this.props.description}
        >
          {this.props.label || this.props.name}
        </label>
        <div className="col-sm-10">
          <Control.checkbox
            model={this.props.model || ' '}
            id={this.props.name}
            name={this.props.name}
            onChange={this.handleChange}
            className="form-control"
            disabled={this.props.disabled}
            required={this.props.required}
          />
        </div>
      </div>
    )
  }
}

CheckboxInput.propTypes = {
  model: PropTypes.string,
  name: PropTypes.string,
  label: PropTypes.string,
  disabled: PropTypes.bool,
  onChange: PropTypes.func,
  required: PropTypes.bool
}

export default CheckboxInput
