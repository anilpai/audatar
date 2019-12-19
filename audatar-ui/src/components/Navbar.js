/* eslint-disable jsx-a11y/href-no-hash */

import React from 'react'
import NavbarUser from './NavbarUser'
import { connect } from 'react-redux'
import { Link } from 'react-router-dom'

class Navbar extends React.Component {
  render() {
    const navButtons = {
      buttons: [
        { path: '/vc', label: 'Validation Check' },
        { path: '/vci', label: 'Validation Check Instance' },
        { path: '/connection', label: 'Connection' }
      ]
    }

    return (
      <div className="collapse header-bce-links navbar-collapse">
        <ul className="nav navbar-nav" role="navigation">
          {this.props.user_props &&
            navButtons.buttons.map(item => (
              <li key={item.label}>
                <Link to={item.path}>
                  <i className={item.icon} /> {item.label}
                </Link>
              </li>
            ))}

          <li className="dropdown">
            <a
              href="#"
              id="help-drop"
              role="button"
              className="dropdown-toggle no-dropdown-backdrop"
              data-toggle="dropdown"
            >
              Help
              <i className="icon-chevron-down" />
            </a>
            <ul
              className="dropdown-menu muted "
              role="menu"
              aria-labelledby="help-drop"
            >
              <li>
                <a
                  href="https://wiki.homeawaycorp.com/x/lBA1F"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Documentation
                </a>
              </li>
            </ul>
          </li>
          <li>
            <a
              href="https://goo.gl/forms/pl0P4bmzXnjBCIKq1"
              target="_blank"
              rel="noopener noreferrer"
            >
              Give Feedback
            </a>
          </li>
          <NavbarUser />
        </ul>
      </div>
    )
  }
}

const mapStateToProps = (state, ownProps) => ({
  user_props: state.auth.user_props
})

export default connect(mapStateToProps)(Navbar)
