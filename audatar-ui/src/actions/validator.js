import axios from 'axios'
import log from '../utils/AppLogger'

export const FETCH_VALIDATOR = 'FETCH_VALIDATOR'
export const FETCH_VALIDATOR_SUCCESS = 'FETCH_VALIDATOR_SUCCESS'
export const FETCH_VALIDATOR_FAILURE = 'FETCH_VALIDATOR_SUCCESS'

export function getValidator(id) {
  return (dispatch, getState) => {
    var validator = getState().validator[id]

    if (!validator || validator.expireTs > new Date().getTime()) {
      var url = `${process.env.REACT_APP_BASE_API_URL}/validator/${id}`

      dispatch({
        type: FETCH_VALIDATOR
      })

      return axios
        .get(url)
        .then(response => {
          dispatch({
            type: FETCH_VALIDATOR_SUCCESS,
            data: response.data
          })
          return response.data
        })
        .catch(error => {
          var errMsg = 'An unknown error has occurred'

          // From https://github.com/axios/axios#handling-errors

          if (error.response) {
            // The request was made and the server responded with a status code
            // that falls out of the range of 2xx
            log.error('Error response data', error.response.data)
            log.error('Error response status', error.response.status)
            log.error('Error response headers', error.response.headers)
            errMsg = error.response.data.msg
          } else if (error.request) {
            // The request was made but no response was received
            // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
            // http.ClientRequest in node.js
            log.error('Error', error.request)
            errMsg = 'No response was received'
          } else {
            // Something happened in setting up the request that triggered an Error
            log.error('Error', error.message)
          }
          dispatch({ type: FETCH_VALIDATOR_FAILURE, errMsg })
        })
    } else {
      return Promise.resolve(validator)
    }
  }
}
