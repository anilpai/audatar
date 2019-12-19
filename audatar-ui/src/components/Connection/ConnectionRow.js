/* eslint-disable jsx-a11y/href-no-hash */

import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { fetchConnectionTypes } from '../../actions/lookup'

class ConnectionRow extends React.Component {
  componentDidMount() {
    this.props.fetchConnectionTypes()
  }

  getConnectionType(connectionTypeId) {
    const connectionType = this.props.connectionTypes.data
    if (connectionType) {
      for (var i = 0; i < connectionType.length; i++) {
        if (connectionType[i].id === connectionTypeId) {
          return connectionType[i].name
        }
      }
    }
    return 'Unknown'
  }

  render() {
    return (
      <tr>
        <td>{this.props.name}</td>
        <td>{this.props.description}</td>
        <td>{this.getConnectionType(this.props.connection_type_id)}</td>
        <td>
          <a href="#">Edit</a>
        </td>
      </tr>
    )
  }
}

ConnectionRow.propTypes = {
  id: PropTypes.number.isRequired,
  name: PropTypes.string.isRequired,
  description: PropTypes.string,
  connection_type_id: PropTypes.number.isRequired
}

const mapStateToProps = state => {
  return {
    connectionTypes: state.lookup.connectionTypes
  }
}

const mapDispatchToProps = dispatch => {
  return bindActionCreators({ fetchConnectionTypes }, dispatch)
}

export default connect(mapStateToProps, mapDispatchToProps)(ConnectionRow)
