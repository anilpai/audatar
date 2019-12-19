import axios from 'axios'
import log from '../utils/AppLogger'

export const LOGIN = 'LOGIN'
export const LOGIN_SUCCESSFULLY = 'LOGIN_SUCCESSFULLY'
export const LOGIN_FAILURE = 'LOGIN_FAILURE'
export const LOG_OUT = 'LOG_OUT'

export function login(user, passwd) {
  return dispatch => {
    dispatch({ type: LOGIN })

    axios
      .post(`${process.env.REACT_APP_BASE_API_URL}/login`, {
        username: user,
        password: passwd
      })
      .then(response => {
        dispatch({
          type: LOGIN_SUCCESSFULLY,
          token: response.data.token,
          username: user.toLowerCase(),
          isAdmin: response.data.isAdmin,
          exp: response.data.exp
        })
      })
      .catch(error => {
        var errMsg = 'An unknown error has occurred'

        // From https://github.com/axios/axios#handling-errors
        if (error.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx
          log.error('Login error response data', error.response.data)
          log.error('Login error response status', error.response.status)
          log.error('Login error response headers', error.response.headers)
          errMsg = error.response.data.msg
        } else if (error.request) {
          // The request was made but no response was received
          // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
          // http.ClientRequest in node.js
          log.error('Login error', error.request)
          errMsg = 'No response was received'
        } else {
          // Something happened in setting up the request that triggered an Error
          log.error('Login error', error.message)
        }
        dispatch({ type: LOGIN_FAILURE, errMsg })
      })
  }
}

export function logout() {
  return dispatch => {
    dispatch({
      type: LOG_OUT
    })
  }
}
