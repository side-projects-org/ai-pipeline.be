import logging

from common import APIException, ErrorCode
from common.awslambda.request_util import get_body
from common.dynamodb.attributes import Attr
from common.dynamodb.model import M

from common.awslambda.response_handler import ResponseHandler

logger = logging.getLogger(__name__)


def validate_request_body(body):
    """
    Validate the request body for required fields.
    :param body: The request body to validate.
    :raises APIException: If required fields are missing.
    """
    required_fields = {"prompt_name", "prompt_version", "response"}
    missing_fields = required_fields - body.keys()

    if missing_fields:
        raise APIException(
            ErrorCode.INVALID_PARAMETER,
            param=", ".join(missing_fields),
        )


@ResponseHandler.api
def lambda_handler(event, context):
    # body 에서 필요한 필드에 대해서 검증한다.
    body = get_body(event)
    validate_request_body(body)

    # prompt_name, prompt_version 으로 Prompt 를 조회한다.
    prompt = M.Prompt.get_item(prompt_name=body['prompt_name'], version=body['prompt_version'])
    if prompt is None:
        raise APIException(ErrorCode.INVALID_PARAMETER, param="prompt_name, version")

    # response 와 prompt 정보를 이용하여 AIResponse 를 저장한다.
    ai_response = save_ai_response(body, prompt)

    return ai_response.to_simple_dict()


def save_ai_response(body:dict, prompt: M.Prompt):
    attr_response_from_ai = Attr.AIResponseAttribute(**body['response'])

    ai_response = M.AIResponse(
        prompt_name=prompt.prompt_name,
        version=prompt.version,
        params=prompt.params,
        response=attr_response_from_ai
    )

    ai_response.save()

    return ai_response