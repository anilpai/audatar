import React from 'react'
import PropTypes from 'prop-types'
import ValidationCheckSearchResultsRow from './ValidationCheckSearchResultsRow'

class ValidationCheckSearchResults extends React.Component {
  render() {
    return (
      <table className="table table-striped">
        <thead className="thead-dark">
          <tr>
            <th>Name</th>
            <th>Team</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {this.props.searchData.map(searchData => {
            return (
              <ValidationCheckSearchResultsRow
                key={searchData.id}
                id={searchData.id}
                name={searchData.name}
                description={searchData.description}
                team_id={searchData.team_id}
              />
            )
          })}
        </tbody>
      </table>
    )
  }
}

ValidationCheckSearchResults.propTypes = {
  searchData: PropTypes.array
}

export default ValidationCheckSearchResults
