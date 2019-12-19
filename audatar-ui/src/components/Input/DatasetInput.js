import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import {AsyncTypeahead} from 'react-bootstrap-typeahead'
import { actions } from 'react-redux-form'
import {getSearchResults} from '../../utils/getDSSuggestions'

class DatasetInput extends React.Component {
  constructor(props) {
      super(props);

      this.state = {
          isLoading: false,
          searchValue: '',
          options: [],
      };

  }

  handleSearch = (searchTerm) => {
    this.setState({
      isLoading: true
    })
    return getSearchResults(searchTerm, `${process.env.REACT_APP_BASE_API_URL}`).then(
      (results) => {
        this.setState({
          isLoading: false,
          options:results.data
        })
        return results;
      }
    );
  }

  handleSelect= (selected) => {
    if (selected) {
        this.searchResultSelected = true;
        let uuid = selected[0] ? selected[0].uuid : ""
        this.props.onSelect(uuid)
    }
    return null;
  }

  renderSearchResultItem(result) {
    return (
        <div>
            <h4>{result.id}</h4>
            <h4>({result.database}) {result.name}</h4>
        </div>
    );
  }

  handleInputChange = searchValue => {
    this.setState({
      searchValue
    });
  }

  render() {
    return (
    <div
      className={
        'form-group row ' +
        ((this.props.ds_suggestions || {}).errMsg ? 'has-error' : '')
      }
    >
      <label
        htmlFor={this.props.name}
        className="col-sm-2 col-form-label control-label"
      >
        {this.props.label || 'Search Dataset by name of uuid'}
      </label>
      <div className="col-sm-10">
        <AsyncTypeahead
          {...this.state}
          labelKey={option =>
            `(${option.database}) ${option.name} [${option.uuid}]`
          }
          minLength={3}
          onSearch={this.handleSearch}
          placeholder="Search datasets ..."
          onChange={
            this.handleSelect
          }
          selected={this.props.selected}
          useCache={false}
          delay={0}
          isLoading={this.state.isLoading}
          renderMenuItemChildren={this.renderSearchResultItem}
        />
      </div>
    </div>
  )
  }
}

DatasetInput.propTypes = {
  model: PropTypes.string,
  name: PropTypes.string,
  label: PropTypes.string,
  disabled: PropTypes.bool,
  onSelect: PropTypes.func,
  includeAllOption: PropTypes.bool,
  setIdOnMount: PropTypes.bool
}

const mapStateToProps = state => {
  return {
    ds_suggestions: state.lookup.ds_suggestions,
    dataset_id: state.validationcheckform.dataset_id
   }
}

const mapDispatchToProps = dispatch => {
  return bindActionCreators(
    {
      idChange: (model, id) => actions.change(model, id)
    },
    dispatch
  )
}

export default connect(mapStateToProps, mapDispatchToProps)(DatasetInput)
