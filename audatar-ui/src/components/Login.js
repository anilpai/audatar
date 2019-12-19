import React from 'react'
import { login, logout } from '../actions/auth'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import BasePage from './BasePage'

class Login extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      username: '',
      password: '',
      submitAttempted: false,
      changedSinceSubmit: false
    }

    this.onSubmit = this.onSubmit.bind(this)
    this.onChange = this.onChange.bind(this)
  }

  onSubmit(e) {
    e.preventDefault()

    if (!this.state.submitAttempted) {
      this.setState({ submitAttempted: true })
    }

    const { username, password } = this.state
    if (username && password) {
      this.setState({ changedSinceSubmit: false })
      this.props.login(username, password)
    }
  }

  onChange(e) {
    this.setState({ [e.target.name]: e.target.value, changedSinceSubmit: true })
  }

  //This is needed to load initial data
  componentDidMount() {
    this.componentWillReceiveProps(this.props)
  }

  //This is needed to load new data if you just change the query parameters in the URL without ever leaving the component
  componentWillReceiveProps(newProps) {
    const search = newProps.location.search // could be '?username=blah'
    const params = new URLSearchParams(search)
    const user = params.get('username')
    if (user !== null) {
      this.setState({ username: user })
    }
  }

  render() {
    return (
      <BasePage
        title="User Login"
        style={{ maxWidth: '400px', margin: '20px auto' }}
      >
        <form onSubmit={this.onSubmit}>
          <div
            className={
              'form-group ' +
              (this.state.submitAttempted && !this.state.username
                ? 'has-error'
                : '')
            }
          >
            <label className="control-label">Username</label>
            <input
              name="username"
              value={this.state.username}
              onChange={this.onChange}
              type="text"
              className="form-control"
            />
          </div>
          <div
            className={
              'form-group ' +
              (this.state.submitAttempted && !this.state.password
                ? 'has-error'
                : '')
            }
          >
            <label className="control-label">Password</label>
            <input
              name="password"
              value={this.state.password}
              onChange={this.onChange}
              type="password"
              className="form-control"
            />
          </div>

          <div className="form-group">
            <button
              className="btn btn-primary btn-lg btn-block"
              disabled={
                this.props.isLoggingIn ||
                !this.state.password ||
                !this.state.username
              }
            >
              {this.props.isLoggingIn ? 'Logging in...' : 'Log in'}
            </button>
          </div>

          {this.props.errMsg &&
            !this.state.changedSinceSubmit && (
              <div className="alert alert-danger">{this.props.errMsg}</div>
            )}
        </form>
      </BasePage>
    )
  }
}

const mapStateToProps = state => {
  return {
    isLoggingIn: state.auth.isLoggingIn,
    errMsg: state.auth.errMsg
  }
}

const mapDispatchToProps = dispatch => {
  return bindActionCreators({ login, logout }, dispatch)
}

export default connect(mapStateToProps, mapDispatchToProps)(Login)
