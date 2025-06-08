from unittest import TestCase

from common.Json import Json


class Test(TestCase):
    def test_lambda_handler(self):
        event = {
            "body": Json.dumps({
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": "Hello, how are you?"}
                ],
                "temperature": 0.7,
                "max_completion_tokens": 150
            }),
        }
        context = {}

        from api.ai.api_post_llm_v2.api_post_llm_v2 import lambda_handler
        response = lambda_handler(event, context)

        print(response)
