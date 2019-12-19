import React from 'react'
import PropTypes from 'prop-types'
import { actions } from 'react-redux-form'
import { connect } from 'react-redux'
import { initialValidationCheckState } from '../../reducers/index'
import ValidationCheckEditNotificationsRow from './ValidationCheckEditNotificationsRow'

class ValidationCheckEditNotifications extends React.Component {
  render() {
    return (
      <div className="form-group row">
        <label className="col-sm-2 col-form-label">Notifications</label>
        <div className="col-sm-10">
          <table className="table table-striped">
            <thead className="thead-dark">
              <tr>
                <th style={{ textAlign: 'center' }}>Success</th>
                <th style={{ textAlign: 'center' }}>Failure</th>
                <th style={{ textAlign: 'center' }}>Error</th>
                <th style={{ textAlign: 'left', width: '15%' }}>Type</th>
                <th style={{ width: '100%' }}>Value</th>
                <th style={{ width: '32px', paddingTop: '0' }}>
                  <button
                    type="button"
                    value="Add"
                    className="btn btn-xs btn-default btn-icon"
                    disabled={this.props.isSaving}
                    onClick={() =>
                      this.props.dispatch(
                        actions.push(
                          'validationcheckform.notifications',
                          initialValidationCheckState.notifications[0]
                        )
                      )
                    }
                  >
                    <i className="icon-plus" aria-hidden="true" />
                  </button>
                </th>
              </tr>
            </thead>
            <tbody>
              {this.props.notifications.map((notification, i) => {
                return (
                  <ValidationCheckEditNotificationsRow
                    id={notification.id}
                    index={i}
                    key={i}
                    disabled={this.props.disabled}
                  />
                )
              })}
            </tbody>
          </table>
        </div>
      </div>
    )
  }
}

ValidationCheckEditNotifications.propTypes = {
  notifications: PropTypes.array.isRequired
}

const mapStateToProps = state => {
  return {
    isSaving: state.validationcheck.save.isSaving
  }
}

export default connect(mapStateToProps)(ValidationCheckEditNotifications)
