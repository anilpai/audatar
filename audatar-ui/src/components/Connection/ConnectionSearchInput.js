import React from 'react'
import PropTypes from 'prop-types'
import ConnectionTypeInput from '../Input/ConnectionTypeInput'
import ConnectionNameInput from '../Input/ConnectionNameInput'

const WAIT_INTERVAL = 1000
const ENTER_KEY = 13

class ConnectionSearchInput extends React.Component {
  constructor(props) {
    super()

    this.searchChange = this.searchChange.bind(this)
    this.state = {
      name: '',
      connectionTypeId: 0
    }
  }

  componentWillMount() {
    this.timer = null
  }

  nameChange = event => {
    clearTimeout(this.timer)
    this.setState({ name: event.target.value })
    this.timer = setTimeout(this.searchChange, WAIT_INTERVAL)
  }

  nameKeyDown = event => {
    if (event.keyCode === ENTER_KEY) {
      event.preventDefault()
      clearTimeout(this.timer)
      this.searchChange()
    }
  }

  connectionTypeSelectionChange = event => {
    clearTimeout(this.timer)
    this.setState({ connectionTypeId: event.target.value }, this.searchChange)
  }

  searchChange() {
    this.props.searchChange(this.state)
  }

  render() {
    return (
      <div className="component-search-input">
        <div>
          <ConnectionTypeInput
            selectionChange={this.connectionTypeSelectionChange}
          />
          <ConnectionNameInput
            nameChange={this.nameChange}
            nameKeyDown={this.nameKeyDown}
          />
        </div>
      </div>
    )
  }
}

ConnectionSearchInput.propTypes = {
  searchChange: PropTypes.func
}

export default ConnectionSearchInput
