import requests

from common import BaseConfig
from common.awslambda.request_util import get_body
from common.awslambda.response_handler import ResponseHandler

@ResponseHandler.api
def lambda_handler(event, context):
    # body 에서 가져온 messages, temperature, max_completion_tokens, model 을 사용하여
    # ChatGPT API 를 호출하여 응답을 받아온다.
    body = get_body(event)

    header = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {BaseConfig.OPEN_AI_KEY}'
    }

    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers=header,
        json={
            'model': body['model'],
            'messages': body['messages'],
            'temperature': body['temperature'],
            'max_tokens': body['max_completion_tokens']
        }
    )

    data = response.json()

    return {
        'params': {
            'model': body['model'],
            'messages': body['messages'],
            'temperature': body['temperature'],
            'max_tokens': body['max_completion_tokens']
        },
        'response': data
    }