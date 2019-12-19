import React from 'react'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { fetchConnectionTypes } from '../../actions/lookup'

function ErrorMessage(props) {
  if ((props.connectionTypes || {}).errMsg) {
    return (
      <span className="help-block">
        Unable to load connectionTypes. Error: {props.connectionTypes.errMsg}
      </span>
    )
  } else {
    return null
  }
}

class ConnectionTypeInput extends React.Component {
  componentDidMount() {
    this.props.fetchConnectionTypes()
  }

  handleChange = event => {
    this.props.selectionChange(event)
  }

  render() {
    return (
      <div
        className={
          'form-group row ' +
          (this.props.connectionTypes && this.props.connectionTypes.errMsg
            ? 'has-error'
            : '')
        }
      >
        <label htmlFor="ConnectionTypeId" className="col-sm-2 col-form-label">
          Connection Types
        </label>
        <div className="col-sm-10">
          <select
            id="ConnectionTypeId"
            name="ConnectionTypeId"
            onChange={this.handleChange}
            className="form-control"
          >
            <option value="0">All Connection Types</option>
            {(this.props.connectionTypes || {}).data &&
              this.props.connectionTypes.data.map(item => {
                return (
                  <option key={item.id} value={item.id}>
                    {' '}
                    {item.name}{' '}
                  </option>
                )
              })}
          </select>
          <ErrorMessage connectionTypes={this.props.connectionTypes} />
        </div>
      </div>
    )
  }
}

const mapStateToProps = state => {
  return { connectionTypes: state.lookup.connectionTypes }
}

const mapDispatchToProps = dispatch => {
  return bindActionCreators({ fetchConnectionTypes }, dispatch)
}

export default connect(mapStateToProps, mapDispatchToProps)(ConnectionTypeInput)
