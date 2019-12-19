import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { fetchDimensions } from '../../actions/lookup'
import { Control, actions } from 'react-redux-form'
import { getDeepProp } from '../../utils/Common'

function ErrorMessage(props) {
  if ((props.dimensions || {}).errMsg) {
    return (
      <span className="help-block">
        Unable to load dimensions. Error: {props.dimensions.errMsg}
      </span>
    )
  } else {
    return null
  }
}

class DimensionInput extends React.Component {
  componentDidMount() {
    this.props.fetchDimensions()
    this.componentWillReceiveProps(this.props)
  }

  componentWillReceiveProps(newProps, dispatch) {
    if (
      this.props.model &&
      getDeepProp(newProps, `dimensions.data`, []).length > 0
    ) {
      this.props.idChange(this.props.model, newProps.dimensions.data[0].id)
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
          ((this.props.dimensions || {}).errMsg ? 'has-error' : '')
        }
      >
        <label
          htmlFor={this.props.name}
          className="col-sm-2 col-form-label control-label"
        >
          {this.props.label || 'Dimension'}
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
            {(this.props.dimensions || {}).data &&
              this.props.dimensions.data.map(item => {
                return (
                  <option key={item.id} value={item.id}>
                    {' '}
                    {item.name}{' '}
                  </option>
                )
              })}
          </Control.select>
          <ErrorMessage dimensions={this.props.dimensions} />
        </div>
      </div>
    )
  }
}

DimensionInput.propTypes = {
  model: PropTypes.string,
  name: PropTypes.string,
  label: PropTypes.string,
  disabled: PropTypes.bool,
  onChange: PropTypes.func
}

const mapStateToProps = state => {
  return { dimensions: state.lookup.dimensions }
}

const mapDispatchToProps = dispatch => {
  return bindActionCreators(
    {
      fetchDimensions,
      idChange: (model, id) => actions.change(model, id)
    },
    dispatch
  )
}

export default connect(mapStateToProps, mapDispatchToProps)(DimensionInput)
