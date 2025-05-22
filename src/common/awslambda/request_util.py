from common import APIException, ErrorCode
from common.Json import Json


def get_query_parameters(event):
    """
    Extracts query parameters from the event object.

    Args:
        event (dict): The event object containing query parameters.

    Returns:
        dict: A dictionary of query parameters.
    """
    if 'queryStringParameters' in event and event['queryStringParameters'] is not None:
        return event['queryStringParameters']
    return {}


def get_query_parameter(event, key: str, default=None):
    """
    Extracts a specific query parameter from the event object.

    Args:
        event (dict): The event object containing query parameters.
        key (str): The key of the query parameter to extract.
        default: The default value to return if the key is not found.

    Returns:
        The value of the query parameter or the default value.
    """
    if 'queryStringParameters' in event and event['queryStringParameters'] is not None:
        return event['queryStringParameters'].get(key, default)
    return default


def get_body(event):
    """
    Extracts the body from the event object.

    Args:
        event (dict): The event object containing the body.

    Returns:
        dict: A dictionary representing the body.
    """
    if 'body' in event and event['body'] is not None:
        return Json.loads(event['body'])

    return {}


def get_path_variable(event, key: str):
    """
    Extracts a specific path variable from the event object.

    Args:
        event (dict): The event object containing path variables.
        key (str): The key of the path variable to extract.

    Returns:
        The value of the path variable
    """
    if 'pathParameters' in event and event['pathParameters'] is not None:
        if key in event['pathParameters']:
            return event['pathParameters'].get(key)

    raise APIException(ErrorCode.PARAMETER_NOT_FOUND, param=key)
