"""Schemas."""
from audatar.extensions import ma


class ConnectionSchema(ma.Schema):
    """Class to serialize Models to JSON."""

    class Meta:
        """Metaclass with settings."""

        fields = ('id', 'name', 'description', 'connection_type_id')

    _links = ma.Hyperlinks({
        'self': ma.URLFor('connection.get_connection_by_id', id='<id>'),
        'collection': ma.URLFor('connection.list_of_connections')
    })


class ConnectionTypeSchema(ma.Schema):
    """Class to serialize Models to JSON."""

    class Meta:
        """Metaclass with settings."""

        fields = ('id', 'name', 'class_path')

    _links = ma.Hyperlinks({
        'self': ma.URLFor('conn_type.get_connectiontype_by_id', id='<id>'),
        'collection': ma.URLFor('conn_type.list_of_connectionstype')
    })


class ConnectionParametersSchema(ma.Schema):
    """Class to serialize Models to JSON."""

    class Meta:
        """Metaclass with settings."""

        fields = ('id', 'connection_id', 'parameter_name', 'parameter_value')

    _links = ma.Hyperlinks({
        'self': ma.URLFor('conn_parameter.get_cp_by_id', id='<id>'),
        'collection': ma.URLFor('conn_parameter.list_all_connection_parameters')
    })


class NotificationsSchema(ma.Schema):
    """Class to serialize Models to JSON."""
    class Meta:
        """Metaclass with settings."""

        fields = ('id', 'validation_check_id', 'notify_if_failure',
                  'notify_if_success', 'notify_if_error', 'value', 'type', 'time_updated', 'updated_by')

    _links = ma.Hyperlinks({
        'self': ma.URLFor('validationcheckparameters.get_vcp_by_id', id='<id>'),
        'collection': ma.URLFor('validationcheckparameters.list_of_validaton_check_parameters')
    })


class ValidationCheckParametersSchema(ma.Schema):
    """Class to serialize Models to JSON."""
    class Meta:
        """Metaclass with settings."""

        fields = ('id', 'validation_check_id',
                  'parameter_name', 'parameter_value', 'time_updated', 'updated_by')

    _links = ma.Hyperlinks({
        'self': ma.URLFor('validationcheckparameters.get_vcp_by_id', id='<id>'),
        'collection': ma.URLFor('validationcheckparameters.list_of_validaton_check_parameters')
    })


class KeywordsSchema(ma.Schema):
    """Class to serialize Models to JSON."""
    class Meta:
        """Metaclass with settings."""

        fields = ('id', 'keyword', 'validation_check_id')

    _links = ma.Hyperlinks({
        'self': ma.URLFor('validationcheckparameters.get_vcp_by_id', id='<id>'),
        'collection': ma.URLFor('validationcheckparameters.list_of_validaton_check_parameters')
    })


class TeamSchema(ma.Schema):
    """Class to serialize Models to JSON."""

    class Meta:
        """Metaclass with settings."""

        fields = ('id', 'name', 'description', 'is_admin')

    _links = ma.Hyperlinks({
        'self': ma.URLFor('team.get_team_by_id', id='<id>'),
        'collection': ma.URLFor('team.list_of_teams')
    })


# class DataSetSchema(ma.Schema):
#     """Class to serialize Models to JSON."""
#
#     class Meta:
#         """Metaclass with settings."""
#
#         fields = ('id', 'name', 'description')
#
#     _links = ma.Hyperlinks({
#         'self': ma.URLFor('dataset.get_dataset_by_id', id='<id>'),
#         'collection': ma.URLFor('dataset.list_of_datasets')
#     })


class VCSchema(ma.Schema):
    """Class to serialize Models to JSON."""
    parameters = ma.Nested(ValidationCheckParametersSchema, many=True, exclude=('validation_check_id', ))
    notifications = ma.Nested(NotificationsSchema, many=True, exclude=('validation_check_id', ))
    keywords = ma.Nested(KeywordsSchema, many=True, exclude=('validation_check_id', ))
    team = ma.Nested(TeamSchema,   only=['name'])

    class Meta:
        """Metaclass with settings."""

        fields = ('id', 'name', 'is_active', 'validator_id', 'description', 'team_id', 'dataset_id', 'dimension_id',
                  'severity_level_id', 'documentation_url', 'cron_schedule', 'time_updated', 'updated_by', 'tags',
                  'parameters', 'notifications', 'keywords', 'team')

    _links = ma.Hyperlinks({
        'self': ma.URLFor('validationcheck.get_vc_by_id', id='<id>'),
        'collection': ma.URLFor('validationcheck.list_of_validation_checks')
    })


class VCISchema(ma.Schema):
    """Class to serialize Models to JSON."""
    vc = ma.Nested(VCSchema, only=['name', 'dataset_id', 'team_id', 'team'])

    class Meta:
        """Metaclass with settings."""

        fields = ('id', 'task_id', 'validation_check_id', 'input', 'time_submitted', 'time_started',
                  'time_completed', 'status', 'result_records', 'result_count', 'created_by', 'result', 'vc',
                  'result_metric', 'sent_to_validation_registry')

    _links = ma.Hyperlinks({
        'self': ma.URLFor('validationcheckinstance.get_vci_by_id', id='<id>'),
        'collection': ma.URLFor('validationcheckinstance.list_of_validation_check_instances')
    })


class ValidatorSchema(ma.Schema):
    """Class to serialize Models to JSON."""

    class Meta:
        """Metaclass with settings."""

        fields = ('id', 'name', 'description', 'class_path')

    _links = ma.Hyperlinks({
        'self': ma.URLFor('validator.get_validator_by_id', id='<id>'),
        'collection': ma.URLFor('validator.list_of_validators')
    })


class NotificationLogSchema(ma.Schema):
    """Class to serialize Models to JSON."""

    class Meta:
        """Metaclass with settings."""

        fields = ('id', 'task_id', 'validation_check_id',
                  'time_completed', 'value', 'type')

    _links = ma.Hyperlinks({
        'self': ma.URLFor('notificationlog.get_notificationlog_by_id', id='<id>'),
        'collection': ma.URLFor('notificationlog.list_of_notificationlog')
    })


class HeartbeatSchema(ma.Schema):
    """Class to serialize Models to JSON."""

    class Meta:
        """Metaclass with settings."""

        fields = ('time', 'interval')

    _links = ma.Hyperlinks({
        'self': ma.URLFor('heartbeat.get_latest_heartbeat', time='<time>'),
        'collection': ma.URLFor('heartbeat.list_of_heartbeats')
    })


class SeverityLevelSchema(ma.Schema):
    """Class to serialize Models to JSON."""

    class Meta:
        """Metaclass with settings."""

        fields = ('id', 'severity_level_order', 'name', 'description')

    _links = ma.Hyperlinks({
        'self': ma.URLFor('severity.get_severitylevel_by_id', id='<id>'),
        'collection': ma.URLFor('severity.list_of_severitylevels')
    })


class DimensionSchema(ma.Schema):
    """Class to serialize Models to JSON."""

    class Meta:
        """Metaclass with settings."""

        fields = ('id', 'name', 'description')

    _links = ma.Hyperlinks({
        'self': ma.URLFor('dimension.get_dimension_by_id', id='<id>'),
        'collection': ma.URLFor('dimension.list_of_dimensions')
    })


conn_schema = ConnectionSchema()
conns_schema = ConnectionSchema(many=True)
conn_type = ConnectionTypeSchema()
conns_type = ConnectionTypeSchema(many=True)
conn_parameters_schema = ConnectionParametersSchema()
conns_parameters_schema = ConnectionParametersSchema(many=True)
vc_schema = VCSchema()
vcs_schema = VCSchema(many=True)
vci_schema = VCISchema()
vcis_schema = VCISchema(many=True)
vcp_schema = ValidationCheckParametersSchema()
vcps_schema = ValidationCheckParametersSchema(many=True)
validator_schema = ValidatorSchema()
validators_schema = ValidatorSchema(many=True)
nl_schema = NotificationLogSchema()
nls_schema = NotificationLogSchema(many=True)
team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)
# dataset_schema = DataSetSchema()
# datasets_schema = DataSetSchema(many=True)
not_schema = NotificationsSchema()
nots_schema = NotificationsSchema(many=True)
heartbeat_schema = HeartbeatSchema()
heartbeats_schema = HeartbeatSchema(many=True)
severitylevel_schema = SeverityLevelSchema()
severitylevels_schema = SeverityLevelSchema(many=True)
dimension_schema = DimensionSchema()
dimensions_schema = DimensionSchema(many=True)
