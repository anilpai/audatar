import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { fetchSeverityLevels } from '../../actions/lookup'
import { Control, actions } from 'react-redux-form'
import { getDeepProp } from '../../utils/Common'

function ErrorMessage(props) {
  if ((props.severitylevels || {}).errMsg) {
    return (
      <span className="help-block">
        Unable to load severity levels. Error: {props.severitylevels.errMsg}
      </span>
    )
  } else {
    return null
  }
}

class SeverityLevelInput extends React.Component {
  componentDidMount() {
    this.props.fetchSeverityLevels()
    this.componentWillReceiveProps(this.props)
  }

  componentWillReceiveProps(newProps, dispatch) {
    if (
      this.props.model &&
      getDeepProp(newProps, `severitylevels.data`, []).length > 0
    ) {
      this.props.idChange(this.props.model, newProps.severitylevels.data[0].id)
    }
  }

  handleChange = event => {
    if (this.props.onChange) {
      this.props.onChange(event)
    }
  }

  render() {
    return (
      <div
        className={
          'form-group row ' +
          ((this.props.severitylevels || {}).errMsg ? 'has-error' : '')
        }
      >
        <label
          htmlFor={this.props.name}
          className="col-sm-2 col-form-label control-label"
        >
          {this.props.label || 'Severity Level'}
        </label>
        <div className="col-sm-10">
          <Control.select
            model={this.props.model || ' '}
            id={this.props.name}
            name={this.props.name}
            onChange={this.handleChange}
            className="form-control"
            disabled={this.props.disabled}
          >
            {(this.props.severitylevels || {}).data &&
              this.props.severitylevels.data.map(item => {
                return (
                  <option key={item.id} value={item.id}>
                    {' '}
                    {item.name}{' '}
                  </option>
                )
              })}
          </Control.select>
          <ErrorMessage severitylevels={this.props.severitylevels} />
        </div>
      </div>
    )
  }
}

SeverityLevelInput.propTypes = {
  model: PropTypes.string,
  name: PropTypes.string,
  label: PropTypes.string,
  disabled: PropTypes.bool,
  onChange: PropTypes.func
}

const mapStateToProps = state => {
  return { severitylevels: state.lookup.severitylevels }
}

const mapDispatchToProps = dispatch => {
  return bindActionCreators(
    {
      fetchSeverityLevels,
      idChange: (model, id) => actions.change(model, id)
    },
    dispatch
  )
}

export default connect(mapStateToProps, mapDispatchToProps)(SeverityLevelInput)
