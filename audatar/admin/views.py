from flask_admin.base import AdminIndexView
from flask_admin.contrib import sqla

from audatar.models import Connection, ConnectionParameter, ConnectionTeamMapping, ConnectionType
from audatar.models import Dimension, Keyword, Team, Notification, NotificationLog
from audatar.models import Validator, ValidationCheck, ValidationCheckParameters, ValidationCheckInstance
from audatar.models import Validgroups
from audatar.extensions import db

admin_view_access = False


class ValidgroupsAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns = ['id', 'group_name']

    def is_accessible(self):
        return admin_view_access


class ConnectionAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns = ['id', 'name', 'description', 'connection_type_id']

    def is_accessible(self):
        return admin_view_access


class ConnectionTypeAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns = ['id', 'name', 'class_path']

    def is_accessible(self):
        return admin_view_access


class ConnectionTeamMappingAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns = ['id', 'connection_id', 'connection', 'team_id', 'team']

    def is_accessible(self):
        return admin_view_access


class ConnectionParameterAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns = ['id', 'connection_id', 'connection', 'parameter_name', 'parameter_value']

    def is_accessible(self):
        return admin_view_access


class VCAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns = ['id', 'name', 'is_active', 'validator_id', 'validator',
                    'description', 'team_id', 'team', 'dataset_id']

    def is_accessible(self):
        return admin_view_access


class VCIAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns = ['id', 'task_id', 'validation_check_id', 'validation_check', 'input', 'status', 'result_records', 'result_count', 'result_metric', 'sent_to_validation_registry']


    def is_accessible(self):
        return admin_view_access


class ValidatorAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns = ['id', 'name', 'description', 'class_path']

    def is_accessible(self):
        return admin_view_access


class VCParametersAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns = ['id', 'validation_check_id', 'validation_check', 'parameter_name', 'parameter_value']

    def is_accessible(self):
        return admin_view_access


class TeamAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns = ['id', 'name', 'description', 'is_admin']

    def is_accessible(self):
        return admin_view_access


# class DataSetAdmin(sqla.ModelView):
#     column_display_pk = True
#     form_columns = ['id', 'name', 'description']
#
#     def is_accessible(self):
#         return admin_view_access


class DimensionAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns = ['id', 'name', 'description']

    def is_accessible(self):
        return admin_view_access


class KeywordAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns = ['id', 'keyword', 'validation_check_id', 'validation_check']

    def is_accessible(self):
        return admin_view_access


class NotificationAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns = ['id', 'validation_check_id', 'validation_check',
                    'notify_if_failure', 'notify_if_success', 'notify_if_error', 'value', 'type']

    def is_accessible(self):
        return admin_view_access


class NotificationLogAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns = ['id', 'validation_check_id', 'task_id', 'time_completed', 'value', 'type']

    def is_accessible(self):
        return admin_view_access


class AdminHomeView(AdminIndexView):
    pass


def admin_routes(admin):
    admin.add_view(ValidgroupsAdmin(Validgroups, db.session, category='validgroups'))
    admin.add_view(VCAdmin(ValidationCheck, db.session, category='validationcheck'))
    admin.add_view(VCIAdmin(ValidationCheckInstance, db.session, category='validationcheck'))
    admin.add_view(ValidatorAdmin(Validator, db.session, category='validator'))
    admin.add_view(VCParametersAdmin(ValidationCheckParameters, db.session, category='validationcheck'))
    admin.add_view(TeamAdmin(Team, db.session, category='team'))
    admin.add_view(DimensionAdmin(Dimension, db.session, category='dimension'))
    admin.add_view(KeywordAdmin(Keyword, db.session, category='keyword'))
    admin.add_view(ConnectionAdmin(Connection, db.session, category='connection'))
    admin.add_view(ConnectionTypeAdmin(ConnectionType, db.session, category='connection'))
    admin.add_view(ConnectionTeamMappingAdmin(ConnectionTeamMapping, db.session, category='connection'))
    admin.add_view(ConnectionParameterAdmin(ConnectionParameter, db.session, category='connection'))
    admin.add_view(NotificationAdmin(Notification, db.session, category='notification'))
    admin.add_view(NotificationLogAdmin(NotificationLog, db.session, category='notification'))
