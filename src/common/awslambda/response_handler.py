import json
import logging

from http import HTTPStatus

from common.APIException import APIException
from common.Json import ClsJsonEncoder

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("common.awslambda.response_handler")


def _api_handler(func):
    def wrapper(*args, **kwargs):
        event = args[0]
        context = args[1]
        logger.info(event)

        try:
            response_data = func(event, context)

            response_body = None
            try:
                # TODO JSON util 로 빼기
                response_body = json.dumps(response_data, cls=ClsJsonEncoder, ensure_ascii=False)
            except Exception as e:
                logger.error(f"JSON serialization error: {e}")
                response_body = e.__cause__

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
            }, cls=ClsJsonEncoder, ensure_ascii=False)

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
