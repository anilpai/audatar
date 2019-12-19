from sqlalchemy.orm import load_only
from audatar.ui.fieldbase import FieldBase
from audatar.models import Connection, ConnectionType


class ConnectionField(FieldBase):
    def __init__(self, parameter_name, label, description, type_filter, name_filter, default_value):
        super().__init__(parameter_name, label, description, default_value)
        self.__type_filter = type_filter
        self.__name_filter = name_filter

    def connections(self):
        type_filter = self.__type_filter
        name_filter = self.__name_filter
        if not type_filter and not name_filter:
            conns_all = Connection.query.options(load_only('name')).all()
            return conns_all
        elif type_filter and not name_filter:
            cn_list = []
            for i in type_filter:
                type_filter_name = i
                ct_idlist = ConnectionType.query.filter(
                    ConnectionType.name == type_filter_name).options(load_only('id')).all()
                for j in ct_idlist:
                    names_list = Connection.query.filter(
                        Connection.connection_type_id == j.id).options(load_only('name')).all()
                    if names_list:
                        cn_list.extend(names_list)
            return cn_list
        elif not type_filter and name_filter:
            cn_list = []
            for i in name_filter:
                names_list = Connection.query.filter(
                    Connection.name == i).options(load_only('name')).all()
                if names_list:
                    cn_list.extend(names_list)
            return cn_list
        else:
            cn_list = []
            for i in name_filter:
                names_list = Connection.query.filter(
                    Connection.name == i).options(load_only('name')).all()
                if names_list:
                    cn_list.extend(names_list)
            return cn_list
