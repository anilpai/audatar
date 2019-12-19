import {
  FETCH_VALIDATOR,
  FETCH_VALIDATOR_SUCCESS,
  FETCH_VALIDATOR_FAILURE
} from '../actions/validator'

const initialState = {
  isFetching: false,
  errMsg: null
}

function validator(state = initialState, action) {
  switch (action.type) {
    case FETCH_VALIDATOR:
      return Object.assign({}, state, {
        isFetching: true,
        errMsg: null
      })
    case FETCH_VALIDATOR_SUCCESS:
      return Object.assign({}, state, {
        isFetching: true,
        errMsg: null,
        [action.data.id]: action.data
      })
    case FETCH_VALIDATOR_FAILURE:
      return Object.assign({}, state, {
        isFetching: false,
        errMsg: action.errMsg
      })
    default:
      return state
  }
}

export default validator
