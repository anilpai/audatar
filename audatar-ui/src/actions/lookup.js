import axios from 'axios'
import log from '../utils/AppLogger'
import { getDeepProp } from '../utils/Common'

export const FETCH_TEAMS = 'FETCH_TEAMS'
export const FETCH_TEAMS_SUCCESS = 'FETCH_TEAMS_SUCCESS'
export const FETCH_TEAMS_FAILURE = 'FETCH_TEAMS_FAILURE'
export const FETCH_DATASETS = 'FETCH_DATASETS'
export const FETCH_DATASETS_SUCCESS = 'FETCH_DATASETS_SUCCESS'
export const FETCH_DATASETS_FAILURE = 'FETCH_DATASETS_FAILURE'
export const FETCH_CONNECTIONTYPES = 'FETCH_CONNECTIONTYPES'
export const FETCH_CONNECTIONTYPES_SUCCESS = 'FETCH_CONNECTIONTYPES_SUCCESS'
export const FETCH_CONNECTIONTYPES_FAILURE = 'FETCH_CONNECTIONTYPES_FAILURE'
export const FETCH_SEVERITYLEVELS = 'FETCH_SEVERITYLEVELS'
export const FETCH_SEVERITYLEVELS_SUCCESS = 'FETCH_SEVERITYLEVELS_SUCCESS'
export const FETCH_SEVERITYLEVELS_FAILURE = 'FETCH_SEVERITYLEVELS_FAILURE'
export const FETCH_VALIDATORS = 'FETCH_VALIDATORS'
export const FETCH_VALIDATORS_SUCCESS = 'FETCH_VALIDATORS_SUCCESS'
export const FETCH_VALIDATORS_FAILURE = 'FETCH_VALIDATORS_FAILURE'
export const FETCH_DIMENSIONS = 'FETCH_DIMENSIONS'
export const FETCH_DIMENSIONS_SUCCESS = 'FETCH_DIMENSIONS_SUCCESS'
export const FETCH_DIMENSIONS_FAILURE = 'FETCH_DIMENSIONS_FAILURE'
export const FETCH_DS_SUGGESTIONS = 'FETCH_DS_SUGGESTIONS'
export const FETCH_DS_SUGGESTIONS_SUCCESS = 'FETCH_DS_SUGGESTIONS_SUCCESS'
export const FETCH_DS_SUGGESTIONS_FAILURE = 'FETCH_DS_SUGGESTIONS_FAILURE'

function sortData(data, sortPropName = 'name') {
  return data.sort(function(a, b) {
    if (a[sortPropName] < b[sortPropName]) return -1
    if (a[sortPropName] > b[sortPropName]) return 1
    return 0
  })
}

function fetchLookup(type) {
  let apiEndpoint, fetchType, successType, failureType

  switch (type) {
    case 'teams':
      apiEndpoint = '/team/'
      fetchType = FETCH_TEAMS
      successType = FETCH_TEAMS_SUCCESS
      failureType = FETCH_TEAMS_FAILURE
      break
    case 'datasets':
      apiEndpoint = '/dataset/'
      fetchType = FETCH_DS_SUGGESTIONS
      successType = FETCH_DS_SUGGESTIONS_SUCCESS
      failureType = FETCH_DS_SUGGESTIONS_FAILURE
      break
    case 'connectionTypes':
      apiEndpoint = '/connectiontype/'
      fetchType = FETCH_CONNECTIONTYPES
      successType = FETCH_CONNECTIONTYPES_SUCCESS
      failureType = FETCH_CONNECTIONTYPES_FAILURE
      break
    case 'severitylevels':
      apiEndpoint = '/severitylevel/'
      fetchType = FETCH_SEVERITYLEVELS
      successType = FETCH_SEVERITYLEVELS_SUCCESS
      failureType = FETCH_SEVERITYLEVELS_FAILURE
      break
    case 'validators':
      apiEndpoint = '/validator/'
      fetchType = FETCH_VALIDATORS
      successType = FETCH_VALIDATORS_SUCCESS
      failureType = FETCH_VALIDATORS_FAILURE
      break
    case 'dimensions':
      apiEndpoint = '/dimension/'
      fetchType = FETCH_DIMENSIONS
      successType = FETCH_DIMENSIONS_SUCCESS
      failureType = FETCH_DIMENSIONS_FAILURE
      break
    default:
      throw new Error(`Unknown lookup type: ${type}`)
  }

  return (dispatch, getState) => {
    var data = getDeepProp(getState(), `lookup.${type}.data`, [])

    if (
      data.length === 0 ||
      getDeepProp(getState(), `lookup.${type}.expireTs`, 0) <
        new Date().getTime()
    ) {
      dispatch({ type: fetchType })

      return axios
        .get(`${process.env.REACT_APP_BASE_API_URL}${apiEndpoint}`)
        .then(response => sortData(response.data.data))
        .then(sorted => {
          dispatch({ type: successType, data: sorted })
          return sorted
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
          dispatch({ type: failureType, errMsg })
        })
    } else {
      return Promise.resolve(data)
    }
  }
}

export function fetchTeams() {
  return fetchLookup('teams')
}

export function fetchDatasets() {
  return fetchLookup('datasets')
}

export function fetchSeverityLevels() {
  return fetchLookup('severitylevels')
}

export function fetchValidators() {
  return fetchLookup('validators')
}

export function fetchConnectionTypes() {
  return fetchLookup('connectionTypes')
}

export function fetchDimensions() {
  return fetchLookup('dimensions')
}

export function fetchDSSuggestions() {
  return fetchLookup('datasets')
}
