/* eslint-disable jsx-a11y/href-no-hash */

import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { Control, actions } from 'react-redux-form'

class ValidationCheckSearchResultsRow extends React.Component {
  render() {
    var valid =
      this.props.form.notifications[this.props.index] &&
      (this.props.form.notifications[this.props.index].value.pristine ||
        this.props.form.notifications[this.props.index].value.valid)

    return (
      <tr className={valid === false ? 'has-error' : ''}>
        <td>
          <Control
            type="hidden"
            model={`validationcheckform.notifications[${this.props.index}].id`}
          />
          <Control.checkbox
            model={`validationcheckform.notifications[${
              this.props.index
            }].notify_if_success`}
            className="form-control center-control"
            disabled={this.props.isSaving}
          />
        </td>
        <td>
          <Control.checkbox
            model={`validationcheckform.notifications[${
              this.props.index
            }].notify_if_failure`}
            className="form-control center-control"
            disabled={this.props.isSaving}
          />
        </td>
        <td>
          <Control.checkbox
            model={`validationcheckform.notifications[${
              this.props.index
            }].notify_if_error`}
            className="form-control center-control"
            disabled={this.props.isSaving}
          />
        </td>
        <td>
          <Control.select
            model={`validationcheckform.notifications[${
              this.props.index
            }].type`}
            className="form-control"
            disabled={this.props.isSaving}
          >
            <option value="Email">Email</option>
            <option value="Webhook">Webhook</option>
          </Control.select>
        </td>
        <td>
          <Control.text
            model={`validationcheckform.notifications[${
              this.props.index
            }].value`}
            className="form-control"
            disabled={this.props.isSaving}
            required
          />
        </td>
        <td>
          <button
            type="button"
            value="Remove"
            className="btn btn-xs btn-default btn-icon"
            disabled={this.props.isSaving}
            onClick={() => {
              // Remove the selected notification
              this.props.dispatch(
                actions.remove(
                  'validationcheckform.notifications',
                  this.props.index
                )
              )
              // Validate if index 1 exists or is not defined
              try {
                if (
                  typeof this.props.form.notifications[1].id === 'undefined'
                ) {
                  throw new Error('undefined')
                }
              } catch (err) {
                // Clear the notifications if removing the last item (if not, the form is left in an invalid state)
                this.props.dispatch(
                  actions.change('validationcheckform.notifications', [])
                )
              }
            }}
          >
            <i className="icon-remove" aria-hidden="true" />
          </button>
        </td>
      </tr>
    )
  }
}

ValidationCheckSearchResultsRow.propTypes = {
  index: PropTypes.number.isRequired
}

const mapStateToProps = state => {
  return {
    isSaving: state.validationcheck.save.isSaving,
    form: state.forms.validationcheckform
  }
}

export default connect(mapStateToProps)(ValidationCheckSearchResultsRow)
