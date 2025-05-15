import json
import uuid
from datetime import datetime

from common import APIException, ErrorCode
from common.pynamo_util import model_to_dict
from common.dynamodb.model import M

from common.awslambda.response_handler import ResponseHandler

from common.dynamodb.model import Prompt

from common.dynamodb.model import AIRequestParamsAttribute

from common.dynamodb.model import AIMessageAttribute

# prompt_name : 프롬프트별 식별값 : string (url 에서 허용되는지 검증)
# version : 프롬프트별 버젼 (Default 는 UTC Current) : string (url 에서 허용되는지 검증)
# model : 일단 GPT 만 지원 : string
# messages : Message[]
# messages[].role : string (user, assistant)
# messages[].content : string
# temperature : 0 ~ 1 : Number
# max_completion_tokens : Number

REQUIRED_KEYS = {"prompt_name", "model", "messages", "temperature", "max_completion_tokens"}
def validate_required_keys(data: dict):
    missing_keys = REQUIRED_KEYS - data.keys()
    if missing_keys:
        raise ValueError(f"Missing required keys: {', '.join(missing_keys)}")

@ResponseHandler.api
def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        validate_required_keys(body)
        key=uuid.uuid4().__str__()
        version =datetime.utcnow().isoformat() if "version" not in body else body["version"]
        # TODO messages 형태도 미리 검증하면 좋을 듯
        prompt = Prompt(
            key=key,
            prompt_name=body["prompt_name"],
            version=version,
            params=AIRequestParamsAttribute(
                model=body["model"],
                messages=[AIMessageAttribute(**msg) for msg in body["messages"]],
                temperature=body["temperature"],
                max_completion_tokens=body["max_completion_tokens"],
                response_format="text",
            ),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        prompt.save()
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Prompt saved successfully", "key": model_to_dict(prompt)},ensure_ascii=False, default=str)
        }
    except ValueError as valueError:
        raise APIException(ErrorCode.PARAMETER_NOT_FOUND, param=str(valueError))
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


