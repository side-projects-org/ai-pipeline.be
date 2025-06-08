from http import HTTPStatus

from pynamodb.exceptions import DoesNotExist

from common import APIException, ErrorCode
from common.awslambda.request_util import get_query_parameter, get_query_parameters
from common.dynamodb.model import M

from common.awslambda.response_handler import ResponseHandler


def validate_request_params(params):
    """
    Validates the request parameters against the required parameters.

    Args:
        params (dict): The request parameters.
        required_params (list): List of required parameter keys.

    Raises:
        APIException: If a required parameter is missing.
    """
    required_params = {'prompt_name', 'version'}
    missing_fields = required_params - params.keys()

    if missing_fields:
        raise APIException(
            ErrorCode.INVALID_PARAMETER,
            params=", ".join(missing_fields)
        )


@ResponseHandler.api
def lambda_handler(event, context):
    params = get_query_parameters(event)
    validate_request_params(params)

    # prompt_name, version 으로 Prompt 를 조회한다.
    prompt = M.Prompt.get_item(prompt_name=params['prompt_name'], version=params['version'])
    if prompt is None:
        raise APIException(ErrorCode.INVALID_PARAMETER, param="prompt_name, version")

    # Prompt 에 해당하는 AIResponse 를 조회한다.
    sk = M.AIResponse.build_sk()
    print(sk)

    ai_responses = M.AIResponse.query(
        hash_key=M.AIResponse.build_pk(prompt.prompt_name),
        range_key_condition=M.AIResponse.sk.startswith(M.AIResponse.build_sk())
    )


    return [res.to_simple_dict() for res in list(ai_responses)]


