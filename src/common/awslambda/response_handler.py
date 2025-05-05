import json
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

            response_body = json.dumps(response_data)

            # TODO response builder 로 빼기
            response = {
                'statusCode': HTTPStatus.OK,
                'headers': {
                    'Content-Type': 'application/json',
                },
                'body': response_body
            }
        except APIException as e:
            logger.error(e.server_log)  # -> 잘못된 파라미터 입력: user_id

            response_body = json.dumps({
                'CODE': e.error_code.name,
                'message': e.message,
                'data': e.kwargs
            })

            response = {
                'statusCode': e.status_code,
                'headers': {
                    'Content-Type': 'application/json',
                },
                'body': response_body,
            }

        return response

    return wrapper


class ResponseHandler:
    api = _api_handler
    worker = _api_handler
