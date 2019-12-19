import React from 'react'
import ConnectionSearchInput from './ConnectionSearchInput'
import ConnectionResults from './ConnectionResults'
import BasePage from '../BasePage'
import log from '../../utils/AppLogger'
import Pager from 'react-pager'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { searchConnections } from '../../actions/search'

const pageSize = 10

class Connection extends React.Component {
  constructor(props) {
    super(props)
    this.handleSearchChange = this.handleSearchChange.bind(this)
    this.handlePageChanged = this.handlePageChanged.bind(this)
    this.state = {
      totalPages: 0,
      currentPage: 0,
      visiblePages: 5,
      criteria: {}
    }
  }

  handlePageChanged(newPage) {
    this.handleSearchChange(this.state.criteria, newPage)
  }

  componentWillReceiveProps(newProps) {
    this.setState({
      totalPages: Math.ceil(newProps.count / pageSize)
    })
  }

  handleSearchChange(criteria, newPage) {
    if (!newPage) {
      newPage = 0
    }

    log.info('Search criteria', criteria)
    this.setState({
      criteria,
      currentPage: newPage
    })

    // Add 1 because the pager is 0-based, but the API is 1-based
    this.props.searchConnections(criteria, newPage + 1, pageSize)
  }

  render() {
    return (
      <BasePage title="Connections">
        <form>
          <ConnectionSearchInput searchChange={this.handleSearchChange} />
          {this.props.data &&
            this.props.data.length > 0 && (
              <div>
                <div className="table-responsive">
                  <ConnectionResults searchData={this.props.data} />
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
                      visiblePages={this.state.visiblePages}
                      className="pagination-sm pull-right"
                      onPageChanged={this.handlePageChanged}
                    />
                  </div>
                </div>
              </div>
            )}
          <div style={{ clear: 'both' }} />
          {this.props.errMsg && (
            <div className="alert alert-danger">{this.props.errMsg}</div>
          )}
          {this.props.warnMsg && (
            <div className="alert alert-warning">{this.props.warnMsg}</div>
          )}
        </form>
      </BasePage>
    )
  }
}

const mapStateToProps = state => {
  return {
    data: state.search.connections.data,
    count: state.search.connections.count,
    errMsg: state.search.connections.errMsg,
    warnMsg: state.search.connections.warnMsg
  }
}

const mapDispatchToProps = dispatch => {
  return bindActionCreators({ searchConnections }, dispatch)
}

export default connect(mapStateToProps, mapDispatchToProps)(Connection)
