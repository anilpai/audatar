/* eslint-disable jsx-a11y/href-no-hash */

import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { fetchTeams, fetchDatasets } from '../../actions/lookup'
import { runValidationCheck } from '../../actions/validationcheck'
import { Link } from 'react-router-dom'
import LoadingImage from '../../images/loading.gif'
import ErrorImage from '../../images/icon-error.png'
import SuccessImage from '../../images/icon-check.png'
import Tooltip from '@homeaway/react-tooltip'

class ValidationCheckSearchResultsRow extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      hasSubmitRun: false
    }
    this.timer = null
  }

  componentDidMount() {
    this.props.fetchTeams()
    this.props.fetchDatasets()
  }

  getTeamName(teamId) {
    const teams = this.props.teams.data
    if (teams) {
      for (var i = 0; i < teams.length; i++) {
        if (teams[i].id === teamId) {
          return teams[i].name
        }
      }
    }
    return 'Unknown'
  }

  runVc = vcId => {
    console.log('Running validation check', vcId)
    this.setState({ hasSubmitRun: true })
    this.props.runValidationCheck(vcId)
  }

  renderRunMsg = () => {
    if (
      this.state.hasSubmitRun &&
      !(this.props.vcRun[this.props.id] || {}).isSubmitting
    ) {
      if ((this.props.vcRun[this.props.id] || {}).errMsg) {
        return (
          <Tooltip
            content={(this.props.vcRun[this.props.id] || {}).errMsg}
            placement="left"
          >
            <img
              src={ErrorImage}
              alt="Error"
              style={{ height: '16px', paddingLeft: '5px' }}
            />
          </Tooltip>
        )
      } else {
        return (
          <Tooltip
            content="Validation check successfully submitted to run"
            placement="left"
          >
            <img
              src={SuccessImage}
              alt="Success"
              style={{ height: '16px', paddingLeft: '5px' }}
            />
          </Tooltip>
        )
      }
    }
  }

  renderRunButton = () => {
    if ((this.props.vcRun[this.props.id] || {}).isSubmitting) {
      return (
        <div style={{ display: 'inline-block' }}>
          <img src={LoadingImage} alt="Loading" style={{ height: '16px' }} />
        </div>
      )
    } else {
      return (
        <a href="#" onClick={() => this.runVc(this.props.id)}>
          Run
        </a>
      )
    }
  }

  render() {
    return (
      <tr>
        <td>{this.props.name}</td>
        <td>{this.getTeamName(this.props.team_id)}</td>
        <td>
          <div>
            <Link to={`/vc/${this.props.id}`}>Edit</Link>
            &nbsp;&nbsp;
            {this.renderRunButton()}
            {this.renderRunMsg()}
          </div>
        </td>
      </tr>
    )
  }
}

ValidationCheckSearchResultsRow.propTypes = {
  id: PropTypes.number.isRequired,
  name: PropTypes.string.isRequired,
  description: PropTypes.string,
  dataset_id: PropTypes.string.isRequired,
  team_id: PropTypes.number.isRequired
}

const mapStateToProps = state => {
  return {
    teams: state.lookup.teams,
    datasets: state.lookup.datasets,
    vcRun: state.validationcheck.run
  }
}

const mapDispatchToProps = dispatch => {
  return bindActionCreators(
    { fetchTeams, fetchDatasets, runValidationCheck },
    dispatch
  )
}

export default connect(mapStateToProps, mapDispatchToProps)(
  ValidationCheckSearchResultsRow
)
