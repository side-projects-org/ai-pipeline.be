from common import APIException, ErrorCode
from common.awslambda.request_util import get_query_parameter
from common.dynamodb.model import Prompt
from common.awslambda.response_handler import ResponseHandler


@ResponseHandler.api
def lambda_handler(event, context):
    prompt_name = get_query_parameter(event, "prompt_name")
    version = get_query_parameter(event, "version")

    try:
        target = get_target_prompts(prompt_name, version)
        result = [prompt.to_simple_dict() for prompt in target]
        return result
    except Exception as e:
        raise APIException(ErrorCode.INTERNAL_ERROR, detail=str(e))


def get_target_prompts(prompt_name: str, version: str):
    # version 기준 검색
    if prompt_name is None:

        if version is None:
            version = "LATEST"

        return Prompt \
        .pk_version_sk_item_type__prompt_name__index \
        .query(
            hash_key = version
        )

    # prompt_name 가 명시된 경우
    else:
        return Prompt \
        .pk_prompt_name_sk_item_type__created_at_index \
        .query(
            hash_key = prompt_name
        )
