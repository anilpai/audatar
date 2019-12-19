import {
  FETCH_VALIDATIONCHECKS,
  FETCH_VALIDATIONCHECKS_SUCCESS,
  FETCH_VALIDATIONCHECKS_FAILURE,
  FETCH_VALIDATIONCHECKINSTANCES,
  FETCH_VALIDATIONCHECKINSTANCES_SUCCESS,
  FETCH_VALIDATIONCHECKINSTANCES_FAILURE,
  FETCH_CONNECTIONS,
  FETCH_CONNECTIONS_SUCCESS,
  FETCH_CONNECTIONS_FAILURE
} from '../actions/search'

const initialState = {
  validationchecks: {
    count: 0,
    data: null,
    pageNumber: 0,
    pageSize: 0,
    isSearching: false,
    errMsg: null,
    warnMsg: null
  },
  validationcheckinstances: {
    count: 0,
    data: null,
    pageNumber: 0,
    pageSize: 0,
    isSearching: false,
    errMsg: null,
    warnMsg: null
  },
  connections: {
    count: 0,
    data: null,
    pageNumber: 0,
    pageSize: 0,
    isSearching: false,
    errMsg: null,
    warnMsg: null
  }
}

function api(state = initialState, action) {
  switch (action.type) {
    case FETCH_VALIDATIONCHECKS:
      return Object.assign({}, state, {
        validationchecks: {
          count: 0,
          data: null,
          pageNumber: 0,
          pageSize: 0,
          isSearching: true,
          errMsg: null,
          warnMsg: null
        }
      })
    case FETCH_VALIDATIONCHECKS_SUCCESS:
      return Object.assign({}, state, {
        validationchecks: {
          count: action.count,
          data: action.data,
          pageNumber: action.pageNumber,
          pageSize: action.pageSize,
          isSearching: false,
          errMsg: null,
          warnMsg: action.count === 0 ? 'No results' : null
        }
      })
    case FETCH_VALIDATIONCHECKS_FAILURE:
      return Object.assign({}, state, {
        validationchecks: {
          count: 0,
          data: null,
          pageNumber: 0,
          pageSize: 0,
          isSearching: false,
          errMsg: action.errMsg,
          warnMsg: null
        }
      })
    case FETCH_VALIDATIONCHECKINSTANCES:
      return Object.assign({}, state, {
        validationcheckinstances: {
          count: 0,
          data: null,
          pageNumber: 0,
          pageSize: 0,
          isSearching: true,
          errMsg: null,
          warnMsg: null
        }
      })
    case FETCH_VALIDATIONCHECKINSTANCES_SUCCESS:
      return Object.assign({}, state, {
        validationcheckinstances: {
          count: action.count,
          data: action.data,
          pageNumber: action.pageNumber,
          pageSize: action.pageSize,
          isSearching: false,
          errMsg: null,
          warnMsg: action.count === 0 ? 'No results' : null
        }
      })
    case FETCH_VALIDATIONCHECKINSTANCES_FAILURE:
      return Object.assign({}, state, {
        validationcheckinstances: {
          count: 0,
          data: null,
          pageNumber: 0,
          pageSize: 0,
          isSearching: false,
          errMsg: action.errMsg,
          warnMsg: null
        }
      })
    case FETCH_CONNECTIONS:
      return Object.assign({}, state, {
        connections: {
          count: 0,
          data: null,
          pageNumber: 0,
          pageSize: 0,
          isSearching: true,
          errMsg: null,
          warnMsg: null
        }
      })
    case FETCH_CONNECTIONS_SUCCESS:
      return Object.assign({}, state, {
        connections: {
          count: action.count,
          data: action.data,
          pageNumber: action.pageNumber,
          pageSize: action.pageSize,
          isSearching: false,
          errMsg: null,
          warnMsg: action.count === 0 ? 'No results' : null
        }
      })
    case FETCH_CONNECTIONS_FAILURE:
      return Object.assign({}, state, {
        connections: {
          count: 0,
          data: null,
          pageNumber: 0,
          pageSize: 0,
          isSearching: false,
          errMsg: action.errMsg,
          warnMsg: null
        }
      })
    default:
      return state
  }
}

export default api
