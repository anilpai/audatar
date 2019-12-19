/* eslint-disable jsx-a11y/href-no-hash */

import React from 'react'
import { logout } from '../actions/auth'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { Link } from 'react-router-dom'

function LoginButton(props) {
  return (
    <li>
      <Link to="/login">Login</Link>
    </li>
  )
}

function LogoutButton(props) {
  return (
    <li className="dropdown">
      <a
        href="#"
        id="traveler-drop"
        role="button"
        className="dropdown-toggle has-avatar"
        data-toggle="dropdown"
      >
        {props.username}
        <i className="icon-chevron-down" />
      </a>
      <ul
        className="dropdown-menu muted "
        role="menu"
        aria-labelledby="user-drop"
      >
        <li>
          <a href="#" onClick={props.onClick}>
            Logout
          </a>
        </li>
      </ul>
    </li>
  )
}

class LoginControl extends React.Component {
  constructor(props) {
    super(props)
    this.handleLogoutClick = this.handleLogoutClick.bind(this)
  }

  handleLogoutClick() {
    this.props.logout()
  }

  render() {
    if (this.props.user_props != null) {
      return (
        <LogoutButton
          onClick={this.handleLogoutClick}
          username={this.props.user_props.username}
        />
      )
    } else {
      return <LoginButton />
    }
  }
}

const mapStateToProps = state => {
  return { user_props: state.auth.user_props }
}

const mapDispatchToProps = dispatch => {
  return bindActionCreators({ logout }, dispatch)
}

export default connect(mapStateToProps, mapDispatchToProps)(LoginControl)
