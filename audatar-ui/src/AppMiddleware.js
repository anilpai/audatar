import log from './utils/AppLogger'
import { getDeepProp } from './utils/Common'
import axios from 'axios'

const logger = store => next => action => {
  //log.info('dispatching', action)
  let result = next(action)
  //log.info('next state', store.getState())
  return result
}

const crashReporter = store => next => action => {
  try {
    return next(action)
  } catch (err) {
    log.error('Caught an exception!', err)
    throw err
  }
}

const axiosHeader = store => next => action => {
  axios.defaults.headers['Authorization'] =
    'Bearer ' + getDeepProp(store.getState(), 'auth.user_props.token')
  return next(action)
}

export { logger, crashReporter, axiosHeader }
