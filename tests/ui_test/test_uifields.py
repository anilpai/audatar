import pytest
from audatar.ui import ConnectionField, TextField, TextAreaField, SelectField


class TestUiFields:

    @pytest.mark.xskip
    def test_connectionfield(self):
        'ui_class() : ConnectionField'
        test_parameter = 'connection'
        test_type_filter = ['SQLAlchemy', 'JDBC']
        test_name_filter = None
        test_default_value = None
        test_connection_field = ConnectionField(test_parameter, test_type_filter, test_name_filter, test_default_value)
        assert test_connection_field is not None

    @pytest.mark.xskip
    def test_selectfield(self):
        'ui_class() : SelectField'
        test_parameter_name = 'pass_condition'
        test_selection_list = [('query returns no results', 'query returns no results'),
                               ('query returns results', 'query returns results')]
        test_allow_multiple = False
        test_select_field = SelectField(test_parameter_name, test_selection_list, test_allow_multiple)
        assert test_select_field is not None

    @pytest.mark.xskip
    def test_textareafield(self):
        'ui_class() : TextAtreaField'
        test_parameter_name = 'query'
        test_rows = 20
        test_default_value = None
        test_area_field = TextAreaField(test_parameter_name, test_rows, test_default_value)
        assert test_area_field is not None

    @pytest.mark.xskip
    def test_textfield(self):
        'ui_class() : TextField'
        test_parameter_name = 'Table'
        test_text_field = TextField(test_parameter_name)
        assert test_text_field is not None
