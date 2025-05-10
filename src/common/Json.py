import datetime
import json
import uuid


class ClsJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        else:
            return super().default(obj)
