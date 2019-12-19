import React from 'react'
import TeamInput from '../Input/TeamInput'
import TextInput from '../Input/TextInput'
import ValidationCheckSearchResults from './ValidationCheckSearchResults'
import BasePage from '../BasePage'
import log from '../../utils/AppLogger'
import Pager from 'react-pager'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { searchValidationChecks } from '../../actions/validationcheck'
import { Link } from 'react-router-dom'

const WAIT_INTERVAL = 1000
const ENTER_KEY = 13
const PAGE_SIZE = 10

class ValidationCheckSearch extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      totalPages: 0,
      currentPage: 0,
      name: '',
      teamId: 0,
      datasetId: 0
    }
    this.timer = null
  }

  componentDidMount() {
    this.componentWillReceiveProps(this.props)
  }

  componentWillReceiveProps(newProps) {
    this.setState({
      totalPages: Math.ceil(newProps.count / PAGE_SIZE),
      currentPage: newProps.pageNumber - 1
    })
  }

  onChange = event => {
    clearTimeout(this.timer)
    this.setState(
      {
        [event.target.name]: event.target.value
      },
      () => {
        // Wait for the user to finish typing before searching
        if (event.target.type === 'text') {
          this.timer = setTimeout(this.searchChange, WAIT_INTERVAL)
        } else {
          this.searchChange()
        }
      }
    )
  }

  onKeyDown = event => {
    if (event.keyCode === ENTER_KEY) {
      event.preventDefault()
      clearTimeout(this.timer)
      this.searchChange()
    }
  }

  searchChange = () => {
    var criteria = {
      name: this.state.name,
      teamId: this.state.teamId,
      datasetId: this.state.datasetId
    }
    log.info('Search criteria changed', criteria)

    this.props.searchValidationChecks(criteria, 1, PAGE_SIZE)
  }

  pageChange = newPage => {
    log.info(`Page changed to ${newPage + 1}`)

    // Add 1 to newPage because the pager is 0-based, but the API is 1-based
    this.props.searchValidationChecks(
      {
        name: this.state.name,
        teamId: this.state.teamId,
        datasetId: this.state.datasetId
      },
      newPage + 1,
      PAGE_SIZE
    )
  }

  render() {
    return (
      <BasePage title="Validation Check">
        <div>
          <form>
            <TeamInput
              onChange={this.onChange}
              name="teamId"
              label="Portfolio"
              includeAllOption
            />
            <TextInput
              onChange={this.onChange}
              onKeyDown={this.onKeyDown}
              name="datasetId"
              label="Dataset UUID"
              tooltip={
                <a href="https://wiki.homeawaycorp.com/x/_M0CGQ">Visit Wiki</a>
              }
            />
            <TextInput
              onChange={this.onChange}
              onKeyDown={this.onKeyDown}
              name="name"
              label="Name"
            />
            {this.props.data &&
              this.props.data.length > 0 && (
                <div>
                  <div className="table-responsive">
                    <ValidationCheckSearchResults
                      searchData={this.props.data}
                    />
                  </div>
                  <div className="form-group row">
                    <div
                      className="col-sm-3"
                      style={{
                        marginTop: '20px',
                        paddingLeft: '20px',
                        color: '#999999'
                      }}
                    >
                      {this.props.count} result{(this.props.count || 0) !== 1 &&
                        's'}
                    </div>
                    <div className="col-sm-9">
                      <Pager
                        total={this.state.totalPages}
                        current={this.state.currentPage}
                        visiblePages={5}
                        onPageChanged={this.pageChange}
                        className="pagination-sm pull-right"
                      />
                    </div>
                  </div>
                </div>
              )}
            <div style={{ clear: 'both' }} />
            <div className="form-group row">
              <div className="col-sm-offset-2 col-sm-10">
                <Link to="/vc/add" className="btn btn-default pull-right">
                  Add Validation Check
                </Link>
                <button
                  type="button"
                  className="btn btn-primary pull-right"
                  style={{ marginRight: '10px' }}
                  onClick={this.searchChange}
                  disabled={this.props.isSearching}
                >
                  {this.props.isSearching ? 'Searching...' : 'Search'}
                </button>
              </div>
            </div>
            {this.props.errMsg && (
              <div className="alert alert-danger">{this.props.errMsg}</div>
            )}
            {this.props.warnMsg && (
              <div className="alert alert-warning">{this.props.warnMsg}</div>
            )}
          </form>
        </div>
      </BasePage>
    )
  }
}

const mapStateToProps = state => {
  return {
    data: state.validationcheck.search.data,
    count: state.validationcheck.search.count,
    pageNumber: state.validationcheck.search.pageNumber,
    errMsg: state.validationcheck.search.errMsg,
    warnMsg: state.validationcheck.search.warnMsg,
    isSearching: state.validationcheck.search.isSearching
  }
}

const mapDispatchToProps = dispatch => {
  return bindActionCreators({ searchValidationChecks }, dispatch)
}

export default connect(mapStateToProps, mapDispatchToProps)(
  ValidationCheckSearch
)
