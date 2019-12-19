import React from 'react'
import ReactDOM from 'react-dom'
import App from './components/App'
import history from './AppHistory'
import store from './AppStore'
import { Provider } from 'react-redux'
import { saveState } from './utils/SessionStorage'

store.subscribe(() => {
  saveState({
    auth: store.getState().auth,
    lookup: store.getState().lookup,
    validator: store.getState().validator
  })
})

ReactDOM.render(
  <Provider store={store}>
    <App history={history} />
  </Provider>,
  document.getElementById('root')
)
