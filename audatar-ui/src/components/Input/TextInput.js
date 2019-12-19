import React from 'react'
import PropTypes from 'prop-types'
import Tooltip from '@homeaway/react-tooltip'
import { Control } from 'react-redux-form'

class TextInput extends React.Component {
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
              <Tooltip tooltipType="popover" content={this.props.tooltip}>
                <i className="icon-info" />
              </Tooltip>
            </div>
          )}
        </div>
        <div className="col-sm-10">
          <Control.text
            model={this.props.model || ' '}
            id={this.props.name}
            name={this.props.name}
            onChange={this.handleChange}
            onKeyDown={this.handleKeyDown}
            className="form-control"
            disabled={this.props.disabled}
            required={this.props.required}
            maxLength={this.props.maxLength}
          />
        </div>
      </div>
    )
  }
}

TextInput.propTypes = {
  model: PropTypes.string,
  name: PropTypes.string,
  label: PropTypes.string,
  disabled: PropTypes.bool,
  onChange: PropTypes.func,
  onKeyDown: PropTypes.func,
  required: PropTypes.bool,
  valid: PropTypes.bool,
  maxLength: PropTypes.number,
  tooltip: PropTypes.oneOfType([
      PropTypes.object,
      PropTypes.string
  ])
}

export default TextInput
