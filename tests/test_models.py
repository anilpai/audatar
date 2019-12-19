import pytest

from audatar.models import ValidationCheck, ValidationCheckInstance, ValidationCheckParameters, Connection, \
    ConnectionParameter, ConnectionTeamMapping, Notification, NotificationLog


class TestValidationCheck:
    @pytest.mark.parametrize(('validation_check_field_name'), {
        'id', 'name', 'is_active', 'validator_id', 'description', 'team_id', 'dataset_id', 'dimension_id',
        'severity_level_id', 'documentation_url'
    })
    def test_mode_has_proper_vc_field(self, validation_check_field_name):
        assert hasattr(ValidationCheck, validation_check_field_name)


class TestValidationCheckInstance:
    @pytest.mark.parametrize(('vci_field_name'), {
        'id', 'task_id', 'validation_check_id', 'input', 'time_submitted', 'time_started',
        'time_completed', 'status', 'result_records', 'result_count', 'created_by', 'result'
    })
    def test_mode_has_proper_vci_field(self, vci_field_name):
        assert hasattr(ValidationCheckInstance, vci_field_name)


class TestValidationCheckParameters:
    @pytest.mark.parametrize(('vcp_field_name'), {
        'id', 'validation_check_id', 'parameter_name', 'parameter_value'
    })
    def test_mode_has_proper_vcp_field(self, vcp_field_name):
        assert hasattr(ValidationCheckParameters, vcp_field_name)


class TestConnection:
    @pytest.mark.parametrize(('connection_field_name'), {
        'id', 'name', 'description', 'connection_type_id'
    })
    def test_mode_has_proper_connection_field(self, connection_field_name):
        assert hasattr(Connection, connection_field_name)


class TestConnectionParameter:
    @pytest.mark.parametrize(('connection_parameter_field_name'), {
        'id', 'connection_id', 'connection', 'parameter_name', 'parameter_value'
    })
    def test_mode_has_proper_connection_parameter_field(self, connection_parameter_field_name):
        assert hasattr(ConnectionParameter, connection_parameter_field_name)


class TestConnectionTeamMapping:
    @pytest.mark.parametrize(('connection_team_mapping_field_name'), {
        'id', 'connection_id', 'connection', 'team_id', 'team'
    })
    def test_mode_has_proper_connection_team_mapping_field(self, connection_team_mapping_field_name):
        assert hasattr(ConnectionTeamMapping, connection_team_mapping_field_name)


class TestNotification:
    @pytest.mark.parametrize(('notification_field_name'), {
        'id', 'validation_check_id', 'validation_check', 'notify_if_failure', 'notify_if_success', 'notify_if_error', 'value', 'type'
    })
    def test_mode_has_proper_notification_field(self, notification_field_name):
        assert hasattr(Notification, notification_field_name)


class TestNotificationLog:
    @pytest.mark.parametrize(('notification_log_field_name'), {
        'id', 'task_id', 'validation_check_id', 'time_completed', 'value', 'type'
    })
    def test_mode_has_proper_notification_log_field(self, notification_log_field_name):
        assert hasattr(NotificationLog, notification_log_field_name)
