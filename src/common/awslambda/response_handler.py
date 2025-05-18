import logging

from http import HTTPStatus

from common.APIException import APIException
from common.Json import Json
from common.dict_util import deep_update

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("common.awslambda.response_handler")


def _api_handler(func):
    def wrapper(*args, **kwargs):
        event = args[0]
        context = args[1]
        logger.info(event)

        response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "isBase64Encoded": False,
            "body": "" # None or ""
        }

        response_data = None
        try:
            # 람다를 실행
            response_data = func(event, context)

            response['body'] = Json.dumps(response_data)
        except APIException as e:
            logger.error(e.server_log)

            deep_update(response, e.build_aws_response())
        except Exception as e:
            logger.error(e)

            deep_update(response, {
                "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
                "body": Json.dumps({
                    "error": str(e)
                })
            })

        return response

    return wrapper


class ResponseHandler:
    api = _api_handler
    worker = _api_handler
