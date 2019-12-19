import React from 'react'

class StartDateInput extends React.Component {
  handleKeyDown = event => {
    this.props.startDateKeyDown(event)
  }

  render() {
    return (
      <div
        className={
          'form-group row ' +
          (this.props.teams && this.props.teams.errMsg ? 'has-error' : '')
        }
      >
        <label htmlFor="StartDate" className="col-sm-2 col-form-label">
          Start Date
        </label>
        <div className="col-sm-10">
          <input
            onKeyDown={this.handleKeyDown}
            className="form-control"
            id="StartDate"
          />
        </div>
      </div>
    )
  }
}

export default StartDateInput
