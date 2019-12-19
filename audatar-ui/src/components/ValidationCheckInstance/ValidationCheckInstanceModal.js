import React from 'react'
import PropTypes from 'prop-types'
import Modal from '@homeaway/react-modal'
import ValidationCheckInstanceModalResult from './ValidationCheckInstanceModalResult'

class ValidationCheckInstanceModal extends React.Component {
  render() {
    return (
      <Modal
        id="modal-validation-check-instance"
        isOpen={this.props.isOpen}
        onClose={this.props.onClose}
        title="Validation Check Instance"
      >
        <ValidationCheckInstanceModalResult
          {...this.props}
          id={this.props.id}
        />
      </Modal>
    )
  }
}

ValidationCheckInstanceModal.propTypes = {
  id: PropTypes.number.isRequired,
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.bool.isRequired
}

export default ValidationCheckInstanceModal
