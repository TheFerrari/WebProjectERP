import json
import logging


class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
        }
        return json.dumps(payload)
