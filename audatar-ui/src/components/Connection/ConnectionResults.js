import React from 'react'
import PropTypes from 'prop-types'
import ConnectionRow from './ConnectionRow'

class ConnectionResults extends React.Component {
  render() {
    return (
      <table className="table table-striped">
        <thead className="thead-dark">
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Connection Type</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {this.props.searchData.map(searchData => {
            return (
              <ConnectionRow
                key={searchData.id}
                id={searchData.id}
                name={searchData.name}
                description={searchData.description}
                connection_type_id={searchData.connection_type_id}
              />
            )
          })}
        </tbody>
      </table>
    )
  }
}

ConnectionResults.propTypes = {
  searchData: PropTypes.array
}

export default ConnectionResults
