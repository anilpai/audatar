import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { fetchTeams } from '../../actions/lookup'
import { Control, actions } from 'react-redux-form'

function ErrorMessage(props) {
  if ((props.teams || {}).errMsg) {
    return (
      <span className="help-block">
        Unable to load teams. Error: {props.teams.errMsg}
      </span>
    )
  } else {
    return null
  }
}

class TeamInput extends React.Component {
  componentDidMount() {
    this.props.fetchTeams().then(data => {
      if (this.props.model && this.props.setIdOnMount) {
        this.props.idChange(
          this.props.model,
          this.props.includeAllOption ? 0 : data[0].id
        )
      }
    })
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
          (this.props.teams && this.props.teams.errMsg ? 'has-error' : '')
        }
      >
        <label
          htmlFor={this.props.name}
          className="col-sm-2 col-form-label control-label"
        >
          {this.props.setIdOnMount}
          {this.props.label || 'Team'}
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
            {this.props.includeAllOption && (
              <option value="0">All Portfolios</option>
            )}
            {(this.props.teams || {}).data &&
              this.props.teams.data.map(item => {
                return (
                  <option key={item.id} value={item.id}>
                    {' '}
                    {item.name}{' '}
                  </option>
                )
              })}
          </Control.select>
          <ErrorMessage teams={this.props.teams} />
        </div>
      </div>
    )
  }
}

TeamInput.propTypes = {
  model: PropTypes.string,
  name: PropTypes.string,
  label: PropTypes.string,
  disabled: PropTypes.bool,
  onChange: PropTypes.func,
  includeAllOption: PropTypes.bool,
  setIdOnMount: PropTypes.bool
}

const mapStateToProps = state => {
  return { teams: state.lookup.teams }
}

const mapDispatchToProps = dispatch => {
  return bindActionCreators(
    {
      fetchTeams,
      idChange: (model, id) => actions.change(model, id)
    },
    dispatch
  )
}

export default connect(mapStateToProps, mapDispatchToProps)(TeamInput)
