import logging

from http import HTTPStatus

from common import APIException

logger = logging.getLogger("common.awslambda.response_handler")


def _api_handler(func):
    def wrapper(*args, **kwargs):
        event = args[0]
        context = args[1]
        logger.info(event)

        try:
            response_data = func(event, context)
            response = {
                'statusCode': HTTPStatus.OK,
                'body': response_data
            }
        except APIException as exc:
            logger.exception(exc)
            response = {
                'statusCode': exc.status_code,
                'body': {
                    'message': exc.message
                }
            }

        return response

    return wrapper


class ResponseHandler:
    api = _api_handler
    worker = _api_handler
