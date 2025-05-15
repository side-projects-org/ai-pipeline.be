import json

from common.pynamo_util import model_to_dict
from common.dynamodb.model import M, Prompt

from common.awslambda.response_handler import ResponseHandler


@ResponseHandler.api
def lambda_handler(event, context):
    # QUERY PARAMETER 에서 key 를 꺼내온다.
    promptName=""
    promptVersion="LATEST"

    try:
        if 'queryStringParameters' in event:
            if 'prompt_name' in event['queryStringParameters']:
                promptName = event['queryStringParameters']['prompt_name']
            if 'version' in event['queryStringParameters']:
                promptVersion = event['queryStringParameters']['version']

        if promptName == "":  # 이름 명시되지 않은 경우
            target = Prompt.prompt_version_created_at_index.query(promptVersion)
        else:  # 이름 명시된 경우
            target = Prompt.prompt_name_version_index.query(promptName,
                                                            Prompt.version == promptVersion)
        print("name", promptName)
        print("ver", promptVersion)
        result = [model_to_dict(prompt) for prompt in target]
        print("result", len(result))
        return json.dumps(result, ensure_ascii=False, default=str)

    except Exception as e:
        return str(e)

