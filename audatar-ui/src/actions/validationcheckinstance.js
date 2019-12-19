import axios from 'axios'
import log from '../utils/AppLogger'
import { actions } from 'react-redux-form'

export const SEARCH_VALIDATIONCHECKINSTANCE = 'SEARCH_VALIDATIONCHECKINSTANCE'
export const SEARCH_VALIDATIONCHECKINSTANCE_SUCCESS =
  'SEARCH_VALIDATIONCHECKINSTANCE_SUCCESS'
export const SEARCH_VALIDATIONCHECKINSTANCE_FAILURE =
  'SEARCH_VALIDATIONCHECKINSTANCE_FAILURE'
export const FETCH_VALIDATIONCHECKINSTANCE = 'FETCH_VALIDATIONCHECKINSTANCE'
export const FETCH_VALIDATIONCHECKINSTANCE_SUCCESS =
  'FETCH_VALIDATIONCHECKINSTANCE_SUCCESS'
export const FETCH_VALIDATIONCHECKINSTANCE_FAILURE =
  'FETCH_VALIDATIONCHECKINSTANCE_FAILURE'
export const SAVE_VALIDATIONCHECKINSTANCE = 'SAVE_VALIDATIONCHECKINSTANCE'
export const SAVE_VALIDATIONCHECKINSTANCE_SUCCESS =
  'SAVE_VALIDATIONCHECKINSTANCE_SUCCESS'
export const SAVE_VALIDATIONCHECKINSTANCE_FAILURE =
  'SAVE_VALIDATIONCHECKINSTANCE_FAILURE'
export const SAVE_VALIDATIONCHECKINSTANCE_CLEAR =
  'SAVE_VALIDATIONCHECKINSTANCE_CLEAR'
export const RUN_VALIDATIONCHECKINSTANCE = 'RUN_VALIDATIONCHECKINSTANCE'
export const RUN_VALIDATIONCHECKINSTANCE_SUCCESS =
  'RUN_VALIDATIONCHECKINSTANCE_SUCCESS'
export const RUN_VALIDATIONCHECKINSTANCE_FAILURE =
  'RUN_VALIDATIONCHECKINSTANCE_FAILURE'

export function searchValidationCheckInstances(criteria, pageNumber, pageSize) {
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
          type: SEARCH_VALIDATIONCHECKINSTANCE_SUCCESS,
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
        dispatch({ type: SEARCH_VALIDATIONCHECKINSTANCE_FAILURE, errMsg })
      })
  }
}

export function getValidationCheckInstance(id) {
  var url = `${process.env.REACT_APP_BASE_API_URL}/vci/${id}`

  return dispatch => {
    dispatch({
      type: FETCH_VALIDATIONCHECKINSTANCE
    })

    return axios
      .get(url)
      .then(response => {
        var validationCheckInstance = response.data

        // Set null fields to default values
        if (!validationCheckInstance.result_records) {
          validationCheckInstance.result_records = ''
        }
        if (!validationCheckInstance.input) {
          validationCheckInstance.input = ''
        }

        dispatch(
          actions.change('validationcheckInstanceform', validationCheckInstance)
        )
        dispatch({
          type: FETCH_VALIDATIONCHECKINSTANCE_SUCCESS,
          data: validationCheckInstance
        })
        return validationCheckInstance
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
        dispatch({ type: FETCH_VALIDATIONCHECKINSTANCE_FAILURE, errMsg })
      })
  }
}
