from http import HTTPStatus

from pynamodb.exceptions import DoesNotExist

from common import APIException, ErrorCode
from common.awslambda.request_util import get_body
from common.dynamodb.model import M

from common.awslambda.response_handler import ResponseHandler


def validate_request_body(body):
    required_fields = {'prompt_name', 'version', 'key'}
    missing_fields = required_fields - body.keys()

    if missing_fields:
        raise APIException(
            ErrorCode.INVALID_PARAMETER,
            param=", ".join(missing_fields)
        )


@ResponseHandler.api
def lambda_handler(event, context):
    # QUERY PARAMETER 에서 key 를 꺼내온다.
    body = get_body(event)

    validate_request_body(body)

    ai_response = M.AiResponse.get_item(
        prompt_name=body['prompt_name'],
        version=body['version'],
        key=body['key']
    )

    if ai_response:
        ai_response.delete()

    return {'message': 'deleted'}
