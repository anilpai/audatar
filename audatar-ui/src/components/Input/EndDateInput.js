import React from 'react'

class EndDateInput extends React.Component {
  handleKeyDown = event => {
    this.props.endDateKeyDown(event)
  }

  render() {
    return (
      <div
        className={
          'form-group row ' +
          (this.props.teams && this.props.teams.errMsg ? 'has-error' : '')
        }
      >
        <label htmlFor="EndDate" className="col-sm-2 col-form-label">
          End Date
        </label>
        <div className="col-sm-10">
          <input
            onKeyDown={this.handleKeyDown}
            className="form-control"
            id="EndDate"
          />
        </div>
      </div>
    )
  }
}

export default EndDateInput
