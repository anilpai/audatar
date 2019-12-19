import datetime
import decimal

from audatar.connections import *


def encode_base(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


def encode_no_connection_details(obj):
    encobj = encode_base(obj)
    if encobj is not None:
        return obj
    elif isinstance(obj, ConnectionBase):
        return obj.__repr__()


def encode_with_connection_details(obj):
    encobj = encode_base(obj)
    if encobj is not None:
        return obj
    elif isinstance(obj, ConnectionBase):
        return {'class': obj.__class__.__name__, 'parameters': obj.parameter_values()}
