import json
from datetime import datetime
from django.http import HttpRequest


REQUIRED_FIELDS = ("model","version","created")
REQUIRED_LENGTH = 2
REQUIRED_TIMESTAMP = "%Y-%m-%d %H:%M:%S"


def validate_json(request: HttpRequest) -> dict | None:
    """ Function for validating the request body """
    # validation for json
    try:
        data = json.loads(request.body)
    except Exception as ex:
        raise ValueError(f'Invalid JSON format: {ex}')
    else:
        if not isinstance(data, dict):
            raise ValueError('Invalid JSON format')

    return data


def validate_robot_creation(request: HttpRequest) -> dict[str, str] | None:
    """ Function for validating the request body fields to create a robot  """
    data = validate_json(request)
    # validation for ("model","version","created")
    for field in REQUIRED_FIELDS:
        if len(data) != len(REQUIRED_FIELDS):
            raise ValueError(f'Request body must match the {REQUIRED_FIELDS} fields')
        elif data.get(field) is None:
            raise TypeError(f'The {field} value is empty')
        elif not isinstance(data[field], str):
            raise TypeError(f'The {field} value is not a string')

    # validation for ("model","version")
    for field in REQUIRED_FIELDS[:2]:
        if len(data[field]) != REQUIRED_LENGTH:
            raise ValueError(f'The {field} value must be an {REQUIRED_LENGTH}-character sequence')
        elif data[field] != data[field].upper():
            raise ValueError(f'The {field} value must be in uppercase')

    # validation for ("created",)
    try:
        timestamp = datetime.strptime(data["created"], REQUIRED_TIMESTAMP)
    except ValueError:
        raise ValueError(f'Timestamp must match the pattern {REQUIRED_TIMESTAMP}')

    return data
