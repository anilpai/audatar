import axios from 'axios'
import log from '../utils/AppLogger'

export const FETCH_VALIDATIONCHECKS = 'FETCH_VALIDATIONCHECKS'
export const FETCH_VALIDATIONCHECKS_SUCCESS = 'FETCH_VALIDATIONCHECKS_SUCCESS'
export const FETCH_VALIDATIONCHECKS_FAILURE = 'FETCH_VALIDATIONCHECKS_FAILURE'
export const FETCH_VALIDATIONCHECKINSTANCES = 'FETCH_VALIDATIONCHECKINSTANCES'
export const FETCH_VALIDATIONCHECKINSTANCES_SUCCESS =
  'FETCH_VALIDATIONCHECKINSTANCES_SUCCESS'
export const FETCH_VALIDATIONCHECKINSTANCES_FAILURE =
  'FETCH_VALIDATIONCHECKINSTANCES_FAILURE'
export const FETCH_CONNECTIONS = 'FETCH_CONNECTIONS'
export const FETCH_CONNECTIONS_SUCCESS = 'FETCH_CONNECTIONS_SUCCESS'
export const FETCH_CONNECTIONS_FAILURE = 'FETCH_CONNECTIONS_FAILURE'

export function searchConnections(criteria, pageNumber, pageSize) {
  var params = []
  if (criteria.name) {
    // Wrap name criteria in % to search all parts of the name
    params.push(`name=%${criteria.name}%`)
  }
  if (criteria.connectionTypeId && criteria.connectionTypeId > 0) {
    params.push(`connection_type_id=${criteria.connectionTypeId}`)
  }

  var url =
    `${process.env.REACT_APP_BASE_API_URL}/connection/?` + params.join('&')

  return dispatch => {
    axios
      .get(url)
      .then(response => {
        dispatch({
          type: FETCH_CONNECTIONS_SUCCESS,
          data: response.data.data
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
        dispatch({ type: FETCH_CONNECTIONS_FAILURE, errMsg: errMsg })
      })
  }
}

export function searchValidationChecks(criteria, pageNumber, pageSize) {
  var params = []
  if (criteria.name) {
    // Wrap name criteria in % to search all parts of the name
    params.push(`name=%${criteria.name}%`)
  }
  if (criteria.teamId && criteria.teamId > 0) {
    params.push(`team_id=${criteria.teamId}`)
  }
  if (criteria.datasetId && criteria.datasetId > 0) {
    params.push(`dataset_id=${criteria.datasetId}`)
  }

  params.push(`pageNumber=${pageNumber}`)
  params.push(`pageSize=${pageSize}`)

  var url = `${process.env.REACT_APP_BASE_API_URL}/vc/?` + params.join('&')

  return dispatch => {
    axios
      .get(url)
      .then(response => {
        dispatch({
          type: FETCH_VALIDATIONCHECKS_SUCCESS,
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
        dispatch({ type: FETCH_VALIDATIONCHECKS_FAILURE, errMsg: errMsg })
      })
  }
}

export function searchValidationCheckInstances(criteria, pageNumber, pageSize) {
  var params = []
  if (criteria.name) {
    // Wrap name criteria in % to search all parts of the name
    params.push(`name=${criteria.name}`)
  }
  if (criteria.teamId && criteria.teamId > 0) {
    params.push(`team_id=${criteria.teamId}`)
  }
  if (criteria.datasetId && criteria.datasetId > 0) {
    params.push(`dataset_id=${criteria.datasetId}`)
  }
  if (criteria.startDate) {
    params.push(`start_date=${criteria.startDate}`)
  }
  if (criteria.endDate) {
    params.push(`end_date=${criteria.endDate}`)
  }

  params.push(`pageNumber=${pageNumber}`)
  params.push(`pageSize=${pageSize}`)

  var url = `${process.env.REACT_APP_BASE_API_URL}/vci/?` + params.join('&')

  return dispatch => {
    axios
      .get(url)
      .then(response => {
        dispatch({
          type: FETCH_VALIDATIONCHECKINSTANCES_SUCCESS,
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
        dispatch({
          type: FETCH_VALIDATIONCHECKINSTANCES_FAILURE,
          errMsg: errMsg
        })
      })
  }
}
