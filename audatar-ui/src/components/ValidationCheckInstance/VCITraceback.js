import React from 'react'
import PropTypes from 'prop-types'
import { Jumbotron } from 'react-bootstrap'

class VCITraceback extends React.Component {
  render() {
    return (
      <div>
        <div>
          <strong>Traceback:</strong>
        </div>
        <Jumbotron>{this.props.result_records}</Jumbotron>
      </div>
    )
  }
}

VCITraceback.propTypes = {
  result_records: PropTypes.object.isRequired
}

export default VCITraceback
