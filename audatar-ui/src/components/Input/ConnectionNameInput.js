import React from 'react'

class ConnectionNameInput extends React.Component {
  handleChange = event => {
    this.props.nameChange(event)
  }

  handleKeyDown = event => {
    this.props.nameKeyDown(event)
  }

  render() {
    return (
      <div
        className={
          'form-group row ' +
          (this.props.name && this.props.name.errMsg ? 'has-error' : '')
        }
      >
        <label htmlFor="Name" className="col-sm-2 col-form-label">
          Name
        </label>
        <div className="col-sm-10">
          <input
            onChange={this.handleChange}
            onKeyDown={this.handleKeyDown}
            className="form-control"
            id="Name"
          />
        </div>
      </div>
    )
  }
}

export default ConnectionNameInput
