import log from '../utils/AppLogger'

export const loadState = () => {
  try {
    const serializedState = sessionStorage.getItem('state')
    if (serializedState === null) {
      return undefined
    }
    return JSON.parse(serializedState)
  } catch (err) {
    log.debug('Error loading state', err)
    return undefined
  }
}

export const saveState = state => {
  try {
    const serializedState = JSON.stringify(state)
    sessionStorage.setItem('state', serializedState)
  } catch (err) {
    log.debug('Error saving state', err)
  }
}
