import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import Logo from '../images/logo.svg'
import Navbar from './Navbar'

class Header extends React.Component {
  render() {
    return (
      <div className="header-bce">
        <div className="container">
          <div className="navbar header navbar-bce">
            <div className="navbar-inner">
              <div className="pull-left">
                <a
                  className="btn-header-collapse"
                  data-toggle="collapse"
                  data-target=".navbar-collapse.header-bce-links"
                >
                  <i className="icon-hamburger-menu" />
                </a>
                <a
                  href="/"
                  title="Audatar"
                  className="logo"
                  style={{ textDecoration: 'none', color: '#000' }}
                >
                  <div>
                    <img className="logo-img" src={Logo} alt="Audatar" />
                    <span className="logo-label">Audatar</span>
                  </div>
                </a>
              </div>

              <Navbar />
            </div>
          </div>

          <div className="header-bce-birdhouse-container birdhouse-toggle">
            <div
              className="flip-container dropdown-toggle"
              data-toggle="dropdown"
            >
              <div className="flipper">
                <div className="front btn-bce">
                  <img
                    alt="birdhouse"
                    src="//csvcus.homeaway.com/rsrcs/cdn-logos/1.9.1/bce/moniker/homeaway_us/birdhouse-bceheader.svg"
                  />
                </div>
                <div className="birdhouse-tagline back">
                  <div>
                    Our
                    <br />Family of
                    <br /> Brands
                  </div>
                </div>
              </div>
            </div>

            <div className="dropdown-menu dropdown-menu-bce-about fade">
              <p>
                HomeAway is the world leader in vacation rentals. We offer the
                largest selection of properties for any travel occasion and
                every budget. We're committed to helping families and friends
                find the perfect vacation rental to create unforgettable travel
                experiences together.
              </p>
              <div>
                <a href="http://www.homeaway.com/info/homeaway/about-the-family">
                  Learn More
                </a>
              </div>
              <div className="text-right bce-about-logo-wrapper">
                <img
                  alt="logo"
                  src="//csvcus.homeaway.com/rsrcs/cdn-logos/1.5.1/bce/brand/homeaway/logo-simple.svg"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

Header.propTypes = {
  logout: PropTypes.object,
  user_props: PropTypes.object
}

const mapStateToProps = (state, ownProps) => ({
  user_props: state.auth.user_props
})

export default connect(mapStateToProps)(Header)
