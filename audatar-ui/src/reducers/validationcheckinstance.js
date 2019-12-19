import {
  SEARCH_VALIDATIONCHECKINSTANCE,
  SEARCH_VALIDATIONCHECKINSTANCE_SUCCESS,
  SEARCH_VALIDATIONCHECKINSTANCE_FAILURE,
  FETCH_VALIDATIONCHECKINSTANCE,
  FETCH_VALIDATIONCHECKINSTANCE_SUCCESS,
  FETCH_VALIDATIONCHECKINSTANCE_FAILURE
} from '../actions/validationcheckinstance'

const initialState = {
  search: {
    count: 0,
    data: null,
    pageNumber: 0,
    pageSize: 0,
    isSearching: false,
    errMsg: null,
    warnMsg: null
  },
  fetch: { data: null, isFetching: false, errMsg: null },
  save: { data: null, isSaving: false, errMsg: null },
  run: []
}

function validationcheckinstance(state = initialState, action) {
  switch (action.type) {
    case SEARCH_VALIDATIONCHECKINSTANCE:
      return Object.assign({}, state, {
        search: {
          count: state.search.count,
          data: state.search.data,
          pageNumber: state.search.pageNumber,
          pageSize: state.search.pageSize,
          isSearching: true,
          errMsg: null,
          warnMsg: null
        }
      })
    case SEARCH_VALIDATIONCHECKINSTANCE_SUCCESS:
      return Object.assign({}, state, {
        search: {
          count: action.count,
          data: action.data,
          pageNumber: action.pageNumber,
          pageSize: action.pageSize,
          isSearching: false,
          errMsg: null,
          warnMsg: action.count === 0 ? 'No results' : null
        }
      })
    case SEARCH_VALIDATIONCHECKINSTANCE_FAILURE:
      return Object.assign({}, state, {
        search: {
          count: 0,
          data: null,
          pageNumber: 0,
          pageSize: 0,
          isSearching: false,
          errMsg: action.errMsg,
          warnMsg: null
        }
      })
    case FETCH_VALIDATIONCHECKINSTANCE:
      return Object.assign({}, state, {
        fetch: {
          data: null,
          isFetching: true,
          errMsg: null
        }
      })
    case FETCH_VALIDATIONCHECKINSTANCE_SUCCESS:
      return Object.assign({}, state, {
        fetch: {
          data: action.data,
          isFetching: false,
          errMsg: null
        }
      })
    case FETCH_VALIDATIONCHECKINSTANCE_FAILURE:
      return Object.assign({}, state, {
        fetch: {
          data: null,
          isFetching: false,
          errMsg: action.errMsg
        }
      })

    default:
      return state
  }
}

export default validationcheckinstance
