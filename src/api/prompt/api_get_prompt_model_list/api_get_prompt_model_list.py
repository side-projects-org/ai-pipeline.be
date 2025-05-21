from common import APIException, ErrorCode
from common.pynamo_util import model_to_dict
from common.dynamodb.model import Prompt

from common.awslambda.response_handler import ResponseHandler


@ResponseHandler.api
def lambda_handler(event, context):
    # QUERY PARAMETER 에서 key 를 꺼내온다.
    try:
        requestPromptName = event.get("queryStringParameters", {}).get("prompt_name", "")
        requestVersion = event.get("queryStringParameters", {}).get("version", "")

        if requestPromptName == "":  # 이름 명시되지 않은 경우
            if requestVersion == "": # 버전 없다면 기본값 LATEST로 검색
                requestVersion="LATEST"
            target = Prompt.version_prompt_name_index.query(requestVersion)
        else:  # 이름 명시된 경우
            if requestVersion == "": # 버전 없다면 해당 프롬프트 이름의 모든 버전 검색
                target = Prompt.prompt_name_version_index.query(requestPromptName)
            else: # 버전 있다면 해당 버전으로 검색
                target = Prompt.prompt_name_version_index.query(requestPromptName,Prompt.version == requestVersion)
        print("name", requestPromptName)
        print("ver", requestVersion)
        # TODO message도 dict 꼴로 전달해야 할지 확인
        result = [model_to_dict(prompt) for prompt in target]
        return result

    except Exception as e:
        raise APIException(ErrorCode.INTERNAL_ERROR,detail=str(e))

