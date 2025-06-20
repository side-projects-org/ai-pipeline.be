import uuid
from datetime import datetime, timezone

from common import APIException, ErrorCode
from common.awslambda.request_util import get_body

from common.awslambda.response_handler import ResponseHandler, logger

from common.dynamodb.model import M, Attr

# prompt_name : 프롬프트별 식별값 : string (url 에서 허용되는지 검증)
# version : 프롬프트별 버젼 (Default 는 UTC Current) : string (url 에서 허용되는지 검증)
# model : 일단 GPT 만 지원 : string
# messages : Message[]
# messages[].role : string (user, assistant)
# messages[].content : string
# temperature : 0 ~ 1 : Number
# max_completion_tokens : Number

REQUIRED_KEYS = {"prompt_name", "model", "messages", "temperature", "max_completion_tokens", "version"}


def validate_required_keys(data: dict):
    missing_keys = REQUIRED_KEYS - data.keys()
    if missing_keys:
        raise ValueError(f"Missing required keys: {', '.join(missing_keys)}")


LATEST_VERSION = "LATEST"
RELEASE_VERSION = "RELEASE"
PROHIBITED_VERSION_NAME = {LATEST_VERSION, RELEASE_VERSION}


def validate_version_name(version: str, prompt_name: str):
    if version in PROHIBITED_VERSION_NAME:
        raise APIException(ErrorCode.INVALID_PARAMETER, param=f"Not Allowed Version Name: {version}")
    # DUPLICATE VERSION ERROR
    item = M.Prompt.get_item(prompt_name, version)
    if item:
        raise APIException(ErrorCode.INVALID_PARAMETER,
                           param=f"Duplicated Version Name: {version} (for prompt: {prompt_name})")


@ResponseHandler.api
def lambda_handler(event, context):
    body = get_body(event)

    validate_required_keys(body)
    # version = datetime.now(timezone.utc).isoformat() if "version" not in body else body["version"]
    version = body["version"]
    prompt_name = body["prompt_name"]
    validate_version_name(version, prompt_name)

    now = datetime.now(timezone.utc)
    # TODO messages 형태도 미리 검증하면 좋을 듯
    prompt = M.Prompt(
        prompt_name=prompt_name,
        version=version,
        params=Attr.AIRequestParamsAttribute(
            model=body["model"],
            messages=[Attr.AIMessageAttribute(**msg) for msg in body["messages"]],
            temperature=body["temperature"],
            max_completion_tokens=body["max_completion_tokens"],
            response_format="text",
        ),
        best_ai=body.get("best_ai", None),
        best_model=body.get("best_model", None),
        updated_at=now,
    )
    prompt.save()

    put_latest_model(prompt)

    data = prompt.to_simple_dict()
    return data


def put_latest_model(prompt: M.Prompt):
    global LATEST_VERSION
    item = M.Prompt.get_item(prompt.prompt_name, LATEST_VERSION)

    if item:
        # 기존 데이터 업데이트
        update_data = {
            "applied_version": prompt.version,
            "params": prompt.params,
            "updated_at": prompt.created_at,
        }
        for key, val in update_data.items():
            setattr(item, key, val)
        item.save()
    else:
        # 새로 생성
        latest_prompt = M.Prompt(
            prompt_name=prompt.prompt_name,
            version=LATEST_VERSION,
            applied_version=prompt.version,
            params=prompt.params,
            created_at=prompt.created_at,
            updated_at=prompt.updated_at,
        )
        latest_prompt.save()
