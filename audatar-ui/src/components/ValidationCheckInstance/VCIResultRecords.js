import React from 'react'
import PropTypes from 'prop-types'
import JsonTable from 'ts-react-json-table'

class VCIResultRecords extends React.Component {
  render() {
    return (
      <div>
        <div>
          <strong>Result Records:</strong>
        </div>
        <JsonTable
          className="table table-striped"
          rows={JSON.parse(this.props.result_records).data}
        />
      </div>
    )
  }
}

VCIResultRecords.propTypes = {
  result_records: PropTypes.object.isRequired
}

export default VCIResultRecords
