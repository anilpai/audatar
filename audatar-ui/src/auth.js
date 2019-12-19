import locationHelperBuilder from 'redux-auth-wrapper/history4/locationHelper'
import { connectedRouterRedirect } from 'redux-auth-wrapper/history4/redirect'

const locationHelper = locationHelperBuilder({})

export const isNotAuthenticated = connectedRouterRedirect({
  authenticatedSelector: state =>
    state.auth.user_props === null ||
    (state.auth.user_props.exp || 0) < new Date().getTime(),
  redirectPath: (state, ownProps) =>
    locationHelper.getRedirectQueryParam(ownProps) || '/',
  allowRedirectBack: false
})

export const isAuthenticated = connectedRouterRedirect({
  authenticatedSelector: state =>
    state.auth.user_props !== null &&
    (state.auth.user_props.exp || 0) >= new Date().getTime(),
  redirectPath: '/login'
})

export const isAdmin = connectedRouterRedirect({
  authenticatedSelector: state =>
    state.auth.user_props !== null && state.auth.user_props.isAdmin,
  predicate: user_props => user_props.isAdmin,
  redirectPath: '/'
})
