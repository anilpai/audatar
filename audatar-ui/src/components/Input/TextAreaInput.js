import React from 'react'
import PropTypes from 'prop-types'
import Tooltip from '@homeaway/react-tooltip'
import { Control } from 'react-redux-form'

class TextAreaInput extends React.Component {
  handleChange = event => {
    if (this.props.onChange) {
      this.props.onChange(event)
    }
  }

  render() {
    return (
      <div
        className={`form-group row ${
          this.props.valid === false ? 'has-error' : ''
        }`}
      >
        <div className="col-sm-2">
          <label
            htmlFor={this.props.name}
            className="col-form-label control-label"
          >
            {this.props.label || this.props.name}
          </label>
          {this.props.tooltip && (
            <div className="input-tooltip">
              <Tooltip content={this.props.tooltip}>
                <i className="icon-info" />
              </Tooltip>
            </div>
          )}
        </div>
        <div className="col-sm-10">
          <Control.textarea
            model={this.props.model || ' '}
            id={this.props.name}
            name={this.props.name}
            onChange={this.handleChange}
            className="form-control"
            rows={this.props.rows || 3}
            placeholder={this.props.placeholder || ''}
            disabled={this.props.disabled}
            required={this.props.required}
            maxLength={this.props.maxLength}
          />
        </div>
      </div>
    )
  }
}

TextAreaInput.propTypes = {
  model: PropTypes.string,
  name: PropTypes.string,
  label: PropTypes.string,
  disabled: PropTypes.bool,
  rows: PropTypes.number,
  placeholder: PropTypes.string,
  onChange: PropTypes.func,
  required: PropTypes.bool,
  valid: PropTypes.bool,
  maxLength: PropTypes.number
}

export default TextAreaInput
