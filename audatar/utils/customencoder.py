from flask import json
from datetime import datetime, time, timedelta


class CustomJSONEncoder(json.JSONEncoder):
    """Custom json Encoder Class that can handle python datetimes."""

    def default(self, obj):
        if isinstance(obj, datetime):
            return datetime.isoformat(obj.replace(microsecond=0))
        if isinstance(obj, time):
            return time.isoformat(obj.replace(microsecond=0))
        if isinstance(obj, timedelta):
            return str(obj)
        return super(CustomJSONEncoder, self).default(obj)
