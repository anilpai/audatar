import {
  LOGIN,
  LOGIN_SUCCESSFULLY,
  LOGIN_FAILURE,
  LOG_OUT
} from '../actions/auth'

const initloginState = {
  user_props: null,
  errMsg: null,
  isLoggingIn: false
}

function auth(state = initloginState, action) {
  switch (action.type) {
    case LOGIN:
      return Object.assign({}, state, {
        user_props: null,
        errMsg: null,
        isLoggingIn: true
      })
    case LOGIN_SUCCESSFULLY:
      return Object.assign({}, state, {
        user_props: {
          token: action.token,
          username: action.username,
          exp: action.exp,
          isAdmin: action.isAdmin
        },
        errmsg: null,
        isLoggingIn: false
      })
    case LOGIN_FAILURE:
      return Object.assign({}, state, {
        user_props: null,
        errMsg: action.errMsg,
        isLoggingIn: false
      })
    case LOG_OUT:
      return Object.assign({}, state, {
        user_props: null,
        errMsg: null,
        isLoggingIn: false
      })
    default:
      return state
  }
}

export default auth
