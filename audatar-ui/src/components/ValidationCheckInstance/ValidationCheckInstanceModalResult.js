import React from 'react'
import PropTypes from 'prop-types'
import VCIResultRecords from './VCIResultRecords'
import VCITraceback from './VCITraceback'

class ValidationCheckInstanceModalResult extends React.Component {
  render() {
    let result = null
    if (this.props.result === 'Error') {
      result = <VCITraceback {...this.props} />
    } else if (this.props.status === 'Success') {
      result = <VCIResultRecords {...this.props} />
    }

    return (
      <div>
        <table className="table table-striped table-responsive">
          <tbody>
            <tr>
              <th>Id</th>
              <td>{this.props.id}</td>
            </tr>
            <tr>
              <th>Task Id</th>
              <td>{this.props.task_id}</td>
            </tr>
            <tr>
              <th>Validation Check Name</th>
              <td>{this.props.vc_name}</td>
            </tr>
            <tr>
              <th>Team Name</th>
              <td>{this.props.team_name}</td>
            </tr>
            <tr>
              <th>Dataset UUID</th>
              <td>{this.props.dataset_id}</td>
            </tr>
            <tr>
              <th>Time Submitted</th>
              <td>{this.props.time_submitted}</td>
            </tr>
            <tr>
              <th>Time Started</th>
              <td>{this.props.time_started}</td>
            </tr>
            <tr>
              <th>Time Completed</th>
              <td>{this.props.time_completed}</td>
            </tr>
            <tr>
              <th>Status</th>
              <td>{this.props.status}</td>
            </tr>
            <tr>
              <th>Result</th>
              <td>{this.props.result}</td>
            </tr>
            <tr>
              <th>Result Count</th>
              <td>{this.props.result_count}</td>
            </tr>
            <tr>
              <th>Created By</th>
              <td>{this.props.created_by}</td>
            </tr>
          </tbody>
        </table>
        <div>
          <strong>Input Parameters:</strong>
        </div>

        <table className="table table-striped table-responsive">
          <tbody>
            {Object.entries(JSON.parse(this.props.input)).map(entry => {
              return (
                <tr>
                  <th>{entry[0]}</th>
                  <td>{entry[1]}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
        <div className="container pre-scrollable">{result}</div>
      </div>
    )
  }
}

ValidationCheckInstanceModalResult.propTypes = {
  id: PropTypes.number.isRequired
}

export default ValidationCheckInstanceModalResult
