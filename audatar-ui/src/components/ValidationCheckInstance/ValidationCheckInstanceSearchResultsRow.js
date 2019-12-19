import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { Button } from '@homeaway/react-buttons'
import ValidationCheckInstanceModal from './ValidationCheckInstanceModal'

class ValidationCheckInstanceSearchResultsRow extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      isOpen: false
    }
  }

  handleOpen = () => {
    this.setState({
      isOpen: true
    })
  }

  handleClose = () => {
    this.setState({
      isOpen: false
    })
  }

  render() {
    return (
      <tr>
        <td>{this.props.id}</td>
        <td>{this.props.vc_name}</td>
        <td>{this.props.team_name}</td>
        <td>{this.props.time_submitted}</td>
        <td>{this.props.time_completed}</td>
        <td>{this.props.status}</td>
        <td>{this.props.result}</td>
        <td>{this.props.result_count}</td>
        <td>
          <Button onClick={this.handleOpen} label="View" />
          <ValidationCheckInstanceModal
            {...this.props}
            id={this.props.id}
            onClose={this.handleClose}
            isOpen={this.state.isOpen}
          />
        </td>
      </tr>
    )
  }
}

ValidationCheckInstanceSearchResultsRow.propTypes = {
  id: PropTypes.number.isRequired,
  task_id: PropTypes.string.isRequired,
  vc_name: PropTypes.string.isRequired,
  time_submitted: PropTypes.instanceOf(Date),
  time_started: PropTypes.instanceOf(Date),
  time_completed: PropTypes.instanceOf(Date),
  status: PropTypes.string.isRequired,
  result: PropTypes.string.isRequired,
  result_count: PropTypes.number,
  created_by: PropTypes.string.isRequired,
  input: PropTypes.object.isRequired
}

export default connect()(ValidationCheckInstanceSearchResultsRow)
