import decimal
import datetime


class JError(Exception):
    pass


def _convertor(v):
    if isinstance(v, datetime.date):
        v = v.isoformat()
    elif isinstance(v, decimal.Decimal):
        v = float(v)
    elif type(v) in ("<class 'jpype._jclass.java.lang.Long'>", "<class 'jpype._jclass.java.lang.Double'>"):
        v = v.value
    return v


def convert_result_list(result):
    for r in result:
        for k, v in r.items():
            r[k] = _convertor(v)
    return result


def convert_tuple(result):
    r = list(result)
    for i, x in enumerate(r):
        r[i] = _convertor(x)
    return tuple(r)
