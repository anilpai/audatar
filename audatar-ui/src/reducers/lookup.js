import {
  FETCH_TEAMS,
  FETCH_TEAMS_SUCCESS,
  FETCH_TEAMS_FAILURE,
  FETCH_DATASETS,
  FETCH_DATASETS_SUCCESS,
  FETCH_DATASETS_FAILURE,
  FETCH_CONNECTIONTYPES,
  FETCH_CONNECTIONTYPES_SUCCESS,
  FETCH_CONNECTIONTYPES_FAILURE,
  FETCH_SEVERITYLEVELS,
  FETCH_SEVERITYLEVELS_SUCCESS,
  FETCH_SEVERITYLEVELS_FAILURE,
  FETCH_VALIDATORS,
  FETCH_VALIDATORS_SUCCESS,
  FETCH_VALIDATORS_FAILURE,
  FETCH_DIMENSIONS,
  FETCH_DIMENSIONS_SUCCESS,
  FETCH_DIMENSIONS_FAILURE,
  FETCH_DS_SUGGESTIONS,
  FETCH_DS_SUGGESTIONS_SUCCESS,
  FETCH_DS_SUGGESTIONS_FAILURE
} from '../actions/lookup'

const EXPIRE_MS = 1800000

const initialState = {
  teams: null,
  datasets: null,
  severitylevels: null,
  validators: null,
  ds_suggestions: null
}

function lookup(state = initialState, action) {
  switch (action.type) {
    case FETCH_TEAMS:
      return Object.assign({}, state, {
        teams: { data: null, errMsg: null, isLoading: true, expireTs: 0 }
      })
    case FETCH_TEAMS_SUCCESS:
      return Object.assign({}, state, {
        teams: {
          data: action.data,
          errMsg: null,
          isLoading: false,
          expireTs: new Date().getTime() + EXPIRE_MS
        }
      })
    case FETCH_TEAMS_FAILURE:
      return Object.assign({}, state, {
        teams: {
          data: null,
          errMsg: action.errMsg,
          isLoading: false,
          expireTs: 0
        }
      })
    case FETCH_DATASETS:
      return Object.assign({}, state, {
        datasets: { data: null, errMsg: null, isLoading: true, expireTs: 0 }
      })
    case FETCH_DATASETS_SUCCESS:
      return Object.assign({}, state, {
        datasets: {
          data: action.data,
          errMsg: null,
          isLoading: false,
          expireTs: new Date().getTime() + EXPIRE_MS
        }
      })
    case FETCH_DATASETS_FAILURE:
      return Object.assign({}, state, {
        datasets: {
          data: null,
          errMsg: action.errMsg,
          isLoading: false,
          expireTs: 0
        }
      })
    case FETCH_SEVERITYLEVELS:
      return Object.assign({}, state, {
        severitylevels: {
          data: null,
          errMsg: null,
          isLoading: true,
          expireTs: 0
        }
      })
    case FETCH_SEVERITYLEVELS_SUCCESS:
      return Object.assign({}, state, {
        severitylevels: {
          data: action.data,
          errMsg: null,
          isLoading: false,
          expireTs: new Date().getTime() + EXPIRE_MS
        }
      })
    case FETCH_SEVERITYLEVELS_FAILURE:
      return Object.assign({}, state, {
        severitylevels: {
          data: null,
          errMsg: action.errMsg,
          isLoading: false,
          expireTs: 0
        }
      })
    case FETCH_VALIDATORS:
      return Object.assign({}, state, {
        validators: { data: null, errMsg: null, isLoading: true, expireTs: 0 }
      })
    case FETCH_VALIDATORS_SUCCESS:
      return Object.assign({}, state, {
        validators: {
          data: action.data,
          errMsg: null,
          isLoading: false,
          expireTs: new Date().getTime() + EXPIRE_MS
        }
      })
    case FETCH_VALIDATORS_FAILURE:
      return Object.assign({}, state, {
        validators: {
          data: null,
          errMsg: action.errMsg,
          isLoading: false,
          expireTs: 0
        }
      })
    case FETCH_DIMENSIONS:
      return Object.assign({}, state, {
        dimensions: { data: null, errMsg: null, isLoading: true, expireTs: 0 }
      })
    case FETCH_DIMENSIONS_SUCCESS:
      return Object.assign({}, state, {
        dimensions: {
          data: action.data,
          errMsg: null,
          isLoading: false,
          expireTs: new Date().getTime() + EXPIRE_MS
        }
      })
    case FETCH_DIMENSIONS_FAILURE:
      return Object.assign({}, state, {
        dimensions: {
          data: null,
          errMsg: action.errMsg,
          isLoading: false,
          expireTs: 0
        }
      })
    case FETCH_CONNECTIONTYPES:
      return Object.assign({}, state, {
        connectionTypes: {
          data: null,
          errMsg: null,
          isLoading: true,
          expireTs: 0
        }
      })
    case FETCH_CONNECTIONTYPES_SUCCESS:
      var connectionTypes = {
        data: action.data,
        errMsg: null,
        isLoading: false,
        expireTs: new Date().getTime() + EXPIRE_MS
      }
      return Object.assign({}, state, {
        connectionTypes
      })
    case FETCH_CONNECTIONTYPES_FAILURE:
      return Object.assign({}, state, {
        connectionTypes: {
          data: null,
          errMsg: action.errMsg,
          isLoading: false,
          expireTs: 0
        }
      })
    case FETCH_DS_SUGGESTIONS:
      return Object.assign({}, state, {
        ds_suggestions : {
          data: null,
          errMsg: null,
          isLoading: true,
          expireTs: 0
        }
      })
    case FETCH_DS_SUGGESTIONS_SUCCESS:
      var ds_suggestions = {
        data: action.data,
        errMsg: null,
        isLoading: false,
        expireTs: new Date().getTime() + EXPIRE_MS
      }
      return Object.assign({}, state, {
        ds_suggestions
      })
    case FETCH_DS_SUGGESTIONS_FAILURE:
      return Object.assign({}, state, {
        ds_suggestions: {
          data: null,
          errMsg: action.errMsg,
          isLoading: false,
          expireTs: 0
        }
      })
    default:
      return state
  }
}

export default lookup
