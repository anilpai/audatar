import axios from 'axios'
import log from '../utils/AppLogger'
import { actions } from 'react-redux-form'
import history from '../AppHistory'

export const SEARCH_VALIDATIONCHECK = 'SEARCH_VALIDATIONCHECK'
export const SEARCH_VALIDATIONCHECK_SUCCESS = 'SEARCH_VALIDATIONCHECK_SUCCESS'
export const SEARCH_VALIDATIONCHECK_FAILURE = 'SEARCH_VALIDATIONCHECK_FAILURE'
export const FETCH_VALIDATIONCHECK = 'FETCH_VALIDATIONCHECK'
export const FETCH_VALIDATIONCHECK_SUCCESS = 'FETCH_VALIDATIONCHECK_SUCCESS'
export const FETCH_VALIDATIONCHECK_FAILURE = 'FETCH_VALIDATIONCHECK_FAILURE'
export const SAVE_VALIDATIONCHECK = 'SAVE_VALIDATIONCHECK'
export const SAVE_VALIDATIONCHECK_SUCCESS = 'SAVE_VALIDATIONCHECK_SUCCESS'
export const SAVE_VALIDATIONCHECK_FAILURE = 'SAVE_VALIDATIONCHECK_FAILURE'
export const SAVE_VALIDATIONCHECK_CLEAR = 'SAVE_VALIDATIONCHECK_CLEAR'
export const RUN_VALIDATIONCHECK = 'RUN_VALIDATIONCHECK'
export const RUN_VALIDATIONCHECK_SUCCESS = 'RUN_VALIDATIONCHECK_SUCCESS'
export const RUN_VALIDATIONCHECK_FAILURE = 'RUN_VALIDATIONCHECK_FAILURE'

export function searchValidationChecks(criteria, pageNumber, pageSize) {
  var params = []
  if (criteria.name) {
    // Wrap name criteria in % to search all parts of the name
    params.push(`name=${criteria.name}`)
  }
  if (criteria.teamId && criteria.teamId > 0) {
    params.push(`team_id=${criteria.teamId}`)
  }
  if (criteria.datasetId) {
    params.push(`dataset_id=${criteria.datasetId}`)
  }

  params.push(`pageNumber=${pageNumber}`)
  params.push(`pageSize=${pageSize}`)

  var url = `${process.env.REACT_APP_BASE_API_URL}/vc/?` + params.join('&')

  return dispatch => {
    dispatch({
      type: SEARCH_VALIDATIONCHECK
    })

    axios
      .get(url)
      .then(response => {
        dispatch({
          type: SEARCH_VALIDATIONCHECK_SUCCESS,
          data: response.data.data,
          count: response.data.count,
          pageNumber: response.data.pageNumber,
          pageSize: response.data.pageSize
        })
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
        dispatch({ type: SEARCH_VALIDATIONCHECK_FAILURE, errMsg })
      })
  }
}

export function getValidationCheck(id) {
  var url = `${process.env.REACT_APP_BASE_API_URL}/vc/${id}`

  return dispatch => {
    dispatch({
      type: FETCH_VALIDATIONCHECK
    })

    return axios
      .get(url)
      .then(response => {
        var validationCheck = response.data

        // Set null fields to default values
        if (!validationCheck.documentation_url) {
          validationCheck.documentation_url = ''
        }
        if (!validationCheck.description) {
          validationCheck.description = ''
        }
        if (!validationCheck.tags) {
          validationCheck.tags = ''
        }

        dispatch(actions.change('validationcheckform', validationCheck))
        dispatch({
          type: FETCH_VALIDATIONCHECK_SUCCESS,
          data: validationCheck
        })
        return validationCheck
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
        dispatch({ type: FETCH_VALIDATIONCHECK_FAILURE, errMsg })
      })
  }
}

export function saveValidationCheck(vc) {
  return dispatch => {
    dispatch({
      type: SAVE_VALIDATIONCHECK
    })

    var validationCheck = JSON.parse(JSON.stringify(vc))
    var errMsg = ''

    // Remove id for new validation check
    if (validationCheck.id === 0) {
      delete validationCheck.id
    }

    validationCheck.notifications.forEach(function(notification) {
      // Remove ids for new notifications
      if (notification.id === 0) {
        delete notification.id
      }
      // Basic validation
      // TODO: Do this somewhere more appropriate
      if (
        !notification.notify_if_success &&
        !notification.notify_if_failure &&
        !notification.notify_if_error
      ) {
        errMsg =
          'All notifications must notify on at least one event (success, failure, error)'
      }
    })

    if (errMsg) {
      dispatch({ type: SAVE_VALIDATIONCHECK_FAILURE, errMsg })
    } else if (validationCheck.id) {
      return axios
        .put(
          `${process.env.REACT_APP_BASE_API_URL}/vc/${validationCheck.id}`,
          validationCheck
        )
        .then(response => {
          //dispatch(actions.change('validationcheckform', response.data));
          dispatch({
            type: SAVE_VALIDATIONCHECK_SUCCESS,
            data: response.data
          })
          setTimeout(() => {
            dispatch({ type: SAVE_VALIDATIONCHECK_CLEAR })
          }, 5000)
          return response.data
        })
        .catch(error => {
          errMsg = 'An unknown error has occurred'

          // From https://github.com/axios/axios#handling-errors

          if (error.response) {
            // The request was made and the server responded with a status code
            // that falls out of the range of 2xx
            log.error('Error response data', error.response.data)
            log.error('Error response status', error.response.status)
            log.error('Error response headers', error.response.headers)
            errMsg = error.response.data.Message
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
          dispatch({ type: SAVE_VALIDATIONCHECK_FAILURE, errMsg })
        })
    } else {
      axios
        .post(`${process.env.REACT_APP_BASE_API_URL}/vc/`, validationCheck)
        .then(response => {
          dispatch(actions.change('validationcheckform.id', response.data.id))
          dispatch({
            type: SAVE_VALIDATIONCHECK_SUCCESS,
            data: response.data
          })
          setTimeout(() => {
            dispatch({ type: SAVE_VALIDATIONCHECK_CLEAR })
          }, 5000)
          history.push(`/vc/${response.data.id}`)
          //history.go();
          return response.data
        })
        .catch(error => {
          errMsg = 'An unknown error has occurred'

          // From https://github.com/axios/axios#handling-errors

          if (error.response) {
            // The request was made and the server responded with a status code
            // that falls out of the range of 2xx
            log.error('Error response data', error.response.data)
            log.error('Error response status', error.response.status)
            log.error('Error response headers', error.response.headers)
            errMsg = error.response.data.Message
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
          dispatch({ type: SAVE_VALIDATIONCHECK_FAILURE, errMsg })
        })
    }
  }
}

export function runValidationCheck(id, optParams) {
  return dispatch => {
    dispatch({
      id,
      type: RUN_VALIDATIONCHECK
    })

    axios
      .post(`${process.env.REACT_APP_BASE_API_URL}/runVC`, {
        validation_check_id: id,
        opts_params: optParams || {}
      })
      .then(response => {
        dispatch({
          id,
          type: RUN_VALIDATIONCHECK_SUCCESS,
          data: response.data
        })
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
        dispatch({ id, type: RUN_VALIDATIONCHECK_FAILURE, errMsg })
      })
  }
}
