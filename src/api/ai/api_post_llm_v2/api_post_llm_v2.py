from openai import OpenAI

from common import BaseConfig

from common.awslambda.request_util import get_body
from common.awslambda.response_handler import ResponseHandler

client = OpenAI(api_key=BaseConfig.OPEN_AI_KEY)

@ResponseHandler.api
def lambda_handler(event, context):
    # body 에서 가져온 messages, temperature, max_completion_tokens, model 을 사용하여
    # ChatGPT API 를 호출하여 응답을 받아온다.
    body = get_body(event)

    response = client.chat.completions.create(model=body['model'],
    messages=body['messages'],
    temperature=body['temperature'],
    max_tokens=body['max_completion_tokens'])

    return {
        'params': {
            'model': body['model'],
            'messages': body['messages'],
            'temperature': body['temperature'],
            'max_tokens': body['max_completion_tokens']
        },
        'response': response.to_dict()
    }
