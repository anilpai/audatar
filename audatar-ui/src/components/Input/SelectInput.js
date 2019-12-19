import React from 'react'
import PropTypes from 'prop-types'
import Tooltip from '@homeaway/react-tooltip'
import { Control } from 'react-redux-form'

class SelectInput extends React.Component {
  handleChange = event => {
    if (this.props.onChange) {
      this.props.onChange(event)
    }
  }

  render() {
    return (
      <div className="form-group row">
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
          <Control.select
            multiple={this.props.allowMultiple}
            model={this.props.model || ' '}
            id={this.props.name}
            name={this.props.name}
            onChange={this.handleChange}
            className="form-control"
            disabled={this.props.disabled}
          >
            {this.props.options &&
              this.props.options.map(item => {
                return (
                  <option key={item.value} value={item.value}>
                    {' '}
                    {item.display}{' '}
                  </option>
                )
              })}
          </Control.select>
        </div>
      </div>
    )
  }
}

SelectInput.propTypes = {
  model: PropTypes.string,
  name: PropTypes.string,
  label: PropTypes.string,
  disabled: PropTypes.bool,
  description: PropTypes.string,
  onChange: PropTypes.func,
  options: PropTypes.array,
  allowMultiple: PropTypes.bool
}

export default SelectInput
