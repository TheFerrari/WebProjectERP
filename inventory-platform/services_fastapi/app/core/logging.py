import json
import logging


def configure_logging():
    class JsonFormatter(logging.Formatter):
        def format(self, record):
            return json.dumps({'level': record.levelname, 'msg': record.getMessage()})

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(logging.INFO)
