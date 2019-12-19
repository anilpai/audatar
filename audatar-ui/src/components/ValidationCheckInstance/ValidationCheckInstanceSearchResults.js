import React from 'react'
import PropTypes from 'prop-types'
import moment from 'moment'
import ValidationCheckInstanceSearchResultsRow from './ValidationCheckInstanceSearchResultsRow'

class ValidationCheckInstanceSearchResults extends React.Component {
  render() {
    return (
      <table className="table table-striped">
        <thead className="thead-dark">
          <tr>
            <th>Id</th>
            <th>Validation Check Name</th>
            <th>Team Name</th>
            <th>Time Submitted</th>
            <th>Time Completed</th>
            <th>Status</th>
            <th>Result</th>
            <th>Result Count</th>
          </tr>
        </thead>
        <tbody>
          {this.props.searchData.map(searchData => {
            return (
              <ValidationCheckInstanceSearchResultsRow
                key={searchData.id}
                id={searchData.id}
                task_id={searchData.task_id}
                vc_name={searchData.vc ? searchData.vc.name : null}
                team_name={searchData.vc ? searchData.vc.team.name : null}
                time_submitted={
                  searchData.time_submitted
                    ? moment(searchData.time_submitted).format(
                        'MMMM Do YYYY, h:mm:ss a CT'
                      )
                    : null
                }
                time_started={
                  searchData.time_started
                    ? moment(searchData.time_started).format(
                        'MMMM Do YYYY, h:mm:ss a CT'
                      )
                    : null
                }
                time_completed={
                  searchData.time_completed
                    ? moment(searchData.time_completed).format(
                        'MMMM Do YYYY, h:mm:ss a CT'
                      )
                    : null
                }
                status={searchData.status}
                result={searchData.result}
                result_count={searchData.result_count}
                created_by={searchData.created_by}
                input={searchData.input}
                result_records={searchData.result_records}
              />
            )
          })}
        </tbody>
      </table>
    )
  }
}

ValidationCheckInstanceSearchResults.propTypes = {
  searchData: PropTypes.array
}

export default ValidationCheckInstanceSearchResults
