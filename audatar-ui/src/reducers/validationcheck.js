import {
  SEARCH_VALIDATIONCHECK,
  SEARCH_VALIDATIONCHECK_SUCCESS,
  SEARCH_VALIDATIONCHECK_FAILURE,
  FETCH_VALIDATIONCHECK,
  FETCH_VALIDATIONCHECK_SUCCESS,
  FETCH_VALIDATIONCHECK_FAILURE,
  SAVE_VALIDATIONCHECK,
  SAVE_VALIDATIONCHECK_SUCCESS,
  SAVE_VALIDATIONCHECK_FAILURE,
  SAVE_VALIDATIONCHECK_CLEAR,
  RUN_VALIDATIONCHECK,
  RUN_VALIDATIONCHECK_SUCCESS,
  RUN_VALIDATIONCHECK_FAILURE
} from '../actions/validationcheck'

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

function validationcheck(state = initialState, action) {
  switch (action.type) {
    case SEARCH_VALIDATIONCHECK:
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
    case SEARCH_VALIDATIONCHECK_SUCCESS:
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
    case SEARCH_VALIDATIONCHECK_FAILURE:
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
    case FETCH_VALIDATIONCHECK:
      return Object.assign({}, state, {
        fetch: {
          data: null,
          isFetching: true,
          errMsg: null
        }
      })
    case FETCH_VALIDATIONCHECK_SUCCESS:
      return Object.assign({}, state, {
        fetch: {
          data: action.data,
          isFetching: false,
          errMsg: null
        }
      })
    case FETCH_VALIDATIONCHECK_FAILURE:
      return Object.assign({}, state, {
        fetch: {
          data: null,
          isFetching: false,
          errMsg: action.errMsg
        }
      })
    case SAVE_VALIDATIONCHECK:
      return Object.assign({}, state, {
        save: {
          data: null,
          isSaving: true,
          isError: false,
          msg: null
        }
      })
    case SAVE_VALIDATIONCHECK_CLEAR:
      return Object.assign({}, state, {
        save: {
          data: null,
          isSaving: false,
          isError: false,
          msg: null
        }
      })
    case SAVE_VALIDATIONCHECK_SUCCESS:
      return Object.assign({}, state, {
        save: {
          data: action.data,
          isSaving: false,
          isError: false,
          msg: 'Successfully saved validation check'
        }
      })
    case SAVE_VALIDATIONCHECK_FAILURE:
      return Object.assign({}, state, {
        save: {
          data: null,
          isSaving: false,
          isError: true,
          msg: action.errMsg
        }
      })
    case RUN_VALIDATIONCHECK:
      return Object.assign({}, state, {
        run: {
          ...state.run,
          [action.id]: {
            isSubmitting: true,
            errMsg: null
          }
        }
      })
    case RUN_VALIDATIONCHECK_SUCCESS:
      return Object.assign({}, state, {
        run: {
          ...state.run,
          [action.id]: {
            isSubmitting: false,
            errMsg: null
          }
        }
      })
    case RUN_VALIDATIONCHECK_FAILURE:
      return Object.assign({}, state, {
        run: {
          ...state.run,
          [action.id]: {
            isSubmitting: false,
            errMsg: action.errMsg
          }
        }
      })
    default:
      return state
  }
}

export default validationcheck
