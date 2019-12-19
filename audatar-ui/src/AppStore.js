import rootReducer from './reducers/index'
import thunk from 'redux-thunk'
import { createStore, compose, applyMiddleware } from 'redux'
import { logger, crashReporter, axiosHeader } from './AppMiddleware'
import { loadState } from './utils/SessionStorage'

const persistedStore = loadState()

const store = createStore(
  rootReducer,
  persistedStore,
  compose(
    applyMiddleware(logger, crashReporter, axiosHeader, thunk),
    window.devToolsExtension ? window.devToolsExtension() : f => f
  )
)

export default store
