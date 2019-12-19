import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { Router, Route, Switch, Redirect } from 'react-router-dom'
import Header from './Header'
import NotFound from './NotFound'
import ValidationCheckSearch from './ValidationCheck/ValidationCheckSearch'
import ValidationCheckEdit from './ValidationCheck/ValidationCheckEdit'
import ValidationCheckInstanceSearch from './ValidationCheckInstance/ValidationCheckInstanceSearch'
import ValidationCheckInstanceView from './ValidationCheckInstance/ValidationCheckInstanceView'
import Connection from './Connection/Connection'
import Login from './Login'
import { isAuthenticated, isNotAuthenticated, isAdmin } from '../auth'
import ReactGA from 'react-ga'

ReactGA.initialize('UA-109690539-3');
function logPageView() {
  ReactGA.set({ page: window.location.pathname + window.location.search });
  ReactGA.pageview(window.location.pathname + window.location.search);
}

class App extends React.Component {
  render() {
    return (
      <Router history={this.props.history}>
        <div>
          <Header />

          <div className="container" style={{ padding: '10px' }}>
            <div className="row">
              {this.props.errors && <div>Error!</div>}
              <Switch>
                <Redirect exact from="/" to="/vc" />
                <Route
                  exact
                  path="/vc"
                  component={isAuthenticated(ValidationCheckSearch)}
                />
                <Route
                  path="/vc/:id"
                  component={isAuthenticated(ValidationCheckEdit)}
                />
                <Route
                  path="/vc/add"
                  component={isAuthenticated(ValidationCheckEdit)}
                />
                <Route
                  path="/connection"
                  component={isAuthenticated(isAdmin(Connection))}
                />
                <Route path="/login" component={isNotAuthenticated(Login)} />
                <Route
                  exact
                  path="/vci"
                  component={isAuthenticated(ValidationCheckInstanceSearch)}
                />
                <Route
                  path="/vci/:id"
                  component={isAuthenticated(ValidationCheckInstanceView)}
                />
                <Route component={NotFound} />
              </Switch>
            </div>
          </div>
        </div>
      </Router>
    )
  }
}

App.propTypes = {
  history: PropTypes.object.isRequired,
  logout: PropTypes.object,
  user_props: PropTypes.object
}

const mapStateToProps = (state, ownProps) => ({
  history: ownProps.history,
  user_props: state.auth.user_props,
  errors: state.errors
})

export default connect(mapStateToProps)(App)
