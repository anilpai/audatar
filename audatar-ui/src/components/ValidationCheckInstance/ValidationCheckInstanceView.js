import React from 'react'
import BasePage from '../BasePage'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { getValidationCheckInstance } from '../../actions/validationcheckinstance'
import VCITraceback from './VCITraceback'
import moment from 'moment'
import JsonTable from 'ts-react-json-table'

class ValidationCheckInstanceView extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      parameters: [],
      show: true,
      originalValidationCheckInstance: {}
    }
  }

  componentDidMount() {
    if (this.props.match.params.id > 0) {
      this.props
        .getValidationCheckInstance(this.props.match.params.id)
        .then(validationCheckInstance => {
          this.setState({
            originalValidationCheckInstance: validationCheckInstance
          })
        })
    }
  }

  render() {
    let result = null
    let input_entries = JSON.stringify(this.props.validationCheckInstance.input)
    if (this.props.validationCheckInstance.result === 'Error') {
      result = <VCITraceback {...this.props.validationCheckInstance} />
    } else if (this.props.validationCheckInstance.status === 'Success') {
      result = (
        <div>
          <div>
            <span><strong>Result Records:</strong></span>
          </div>
          <JsonTable
            className="table table-striped"
            rows={JSON.parse(JSON.stringify(this.props.validationCheckInstance.result_records)).data}
          />
        </div>
      )
    }

    return (
      <div>
        <BasePage title="Validation Check Instance">
          <div>
            <table className="table table-striped table-responsive">
              <tbody>
                <tr>
                  <th>Id</th>
                  <td>{this.props.validationCheckInstance.id}</td>
                </tr>
                <tr>
                  <th>Task Id</th>
                  <td>{this.props.validationCheckInstance.task_id}</td>
                </tr>
                <tr>
                  <th>Validation Check Name</th>
                  <td>
                    {this.props.validationCheckInstance.vc
                      ? this.props.validationCheckInstance.vc.name
                      : null}
                  </td>
                </tr>
                <tr>
                  <th>Team Name</th>
                  <td>
                    {this.props.validationCheckInstance.vc
                      ? this.props.validationCheckInstance.vc.team.name
                      : null}
                  </td>
                </tr>
                <tr>
                  <th>Time Submitted</th>
                  <td>
                    {this.props.validationCheckInstance.time_submitted
                      ? moment(
                          this.props.validationCheckInstance.time_submitted
                        ).format('MMMM Do YYYY, h:mm:ss a CT')
                      : null}
                  </td>
                </tr>
                <tr>
                  <th>Time Started</th>
                  <td>
                    {this.props.validationCheckInstance.time_started
                      ? moment(
                          this.props.validationCheckInstance.time_started
                        ).format('MMMM Do YYYY, h:mm:ss a CT')
                      : null}
                  </td>
                </tr>
                <tr>
                  <th>Time Completed</th>
                  <td>
                    {this.props.validationCheckInstance.time_completed
                      ? moment(
                          this.props.validationCheckInstance.time_completed
                        ).format('MMMM Do YYYY, h:mm:ss a CT')
                      : null}
                  </td>
                </tr>
                <tr>
                  <th>Status</th>
                  <td>{this.props.validationCheckInstance.status}</td>
                </tr>
                <tr>
                  <th>Result</th>
                  <td>{this.props.validationCheckInstance.result}</td>
                </tr>
                <tr>
                  <th>Result Count</th>
                  <td>{this.props.validationCheckInstance.result_count}</td>
                </tr>
                <tr>
                  <th>Input</th>
                  <td>{input_entries}</td>
                </tr>
                <tr>
                  <th>Created By</th>
                  <td>{this.props.validationCheckInstance.created_by}</td>
                </tr>
              </tbody>
            </table>
            <div className="container pre-scrollable">{result}</div>
          </div>
        </BasePage>
      </div>
    )
  }
}

const mapStateToProps = state => {
  return {
    id: PropTypes.number.isRequired,
    data: state.validationcheck.save.data,
    msg: state.validationcheck.save.msg,
    isError: state.validationcheck.save.isError,
    isSaving: state.validationcheck.save.isSaving,
    validationCheckInstance: state.validationcheckInstanceform,
    form: state.forms.validationcheckInstanceform,
    isFetching: state.validationcheck.fetch.isFetching,
    onClose: PropTypes.bool.isRequired,
    isOpen: PropTypes.bool.isRequired,
    searchData: PropTypes.array,
    input: PropTypes.object.isRequired
  }
}

const mapDispatchToProps = dispatch => {
  return bindActionCreators({ getValidationCheckInstance }, dispatch)
}

export default connect(mapStateToProps, mapDispatchToProps)(
  ValidationCheckInstanceView
)
