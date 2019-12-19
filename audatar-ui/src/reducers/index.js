import auth from './auth'
import lookup from './lookup'
import validationcheck from './validationcheck'
import validationcheckinstance from './validationcheckinstance'
import validator from './validator'
import search from './search'
import { combineReducers } from 'redux'
import { createForms } from 'react-redux-form'

export const initialValidationCheckState = {
  id: 0,
  name: '',
  description: '',
  team_id: 0,
  dataset_id: '',
  severity_level_id: 0,
  validator_id: 0,
  dimension_id: 1,
  parameters: [],
  notifications: [
    {
      id: 0,
      notify_if_error: false,
      notify_if_failure: false,
      notify_if_success: false,
      type: '',
      value: ''
    }
  ],
  documentation_url: '',
  is_active: false,
  keywords: []
}

export const initialValidationCheckSearchState = {
  name: '',
  team_id: 0,
  dataset_id: ''
}

export const initialValidationCheckInstanceState = {
  id: 0,
  name: '',
  description: '',
  team_id: 0,
  dataset_id: ''
}

export default combineReducers({
  auth,
  lookup,
  validationcheck,
  validationcheckinstance,
  validator,
  search,
  ...createForms({
    validationcheckform: initialValidationCheckState,
    validationchecksearchform: initialValidationCheckSearchState,
    validationcheckInstanceform: initialValidationCheckInstanceState
  })
})
