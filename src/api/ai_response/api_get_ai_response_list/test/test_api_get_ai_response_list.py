import unittest
from unittest import TestCase

from api.ai_response.api_get_ai_response_list.api_get_ai_response_list import validate_request_params, lambda_handler
from common import APIException, ErrorCode
from common.Json import Json
from common.dynamodb.attributes import Attr, AiMessageAttribute
from common.dynamodb.model import M


class Test(TestCase):


    def tearDown(self):
        prompt = M.Prompt.get_item('test_prompt', '1.0')

        if prompt:
            prompt.delete()

        ai_responses = M.AiResponse.query(
            hash_key='test_prompt',
            range_key_condition=M.AiResponse.sk.startswith(M.AiResponse.build_sk())
        )

        for ai_response in ai_responses:
            ai_response.delete()

    def test_validate_request_query_params(self):
        query_params = {
            'prompt_name': 'test_prompt',
            'version': '1.0',
        }

        validate_request_params(query_params)

        self.assertEqual(1, 1)

    def test_validate_request_query_params_missing(self):
        query_params = {
            'prompt_name': 'test_prompt',
        }

        with self.assertRaises(APIException) as context:
            validate_request_params(query_params)

        self.assertEqual(context.exception.error_code, ErrorCode.INVALID_PARAMETER)
        self.assertEqual(context.exception.kwargs['params'], 'version')


    def test_lambda_handler(self):
        # given
        prompt = M.Prompt(
            prompt_name='test_prompt',
            version='1.0',
            params=Attr.AiRequestParamsAttribute(
                messages=[
                    AiMessageAttribute(role="user", content="Hello, how are you?")
                ],
                max_tokens=100,
                max_completions_tokens=100,
                model='gpt-3.5-turbo',
                temperature=0.7,
            )
        )

        prompt.save()

        ai_responses = [
            Attr.AnswerAttribute(
                id=f'response_{x}',
                object='chat.completion',
                created=1234567890 + x,
                model='gpt-3.5-turbo',
                usage=Attr.AnswerUsageAttribute(
                    prompt_tokens=10 + x,
                    completion_tokens=20 + x,
                    total_tokens=30 + x
                ),
                choices=[
                    Attr.ChoiceAttribute(
                        index=0,
                        message=AiMessageAttribute(role='assistant', content=f'Response {x}'),
                        finish_reason='stop'
                    )
                ],
            ) for x in range(5)
        ]

        for ai_response in ai_responses:
            ai_response_item = M.AiResponse(
                prompt_name=prompt.prompt_name,
                version=prompt.version,
                params=prompt.params,
                answer=ai_response
            )
            ai_response_item.save()

            print(ai_response_item.pk, ai_response_item.sk)



        event = {
            'queryStringParameters': {
                'prompt_name': 'test_prompt',
                'version': '1.0',
            }
        }

        context = None

        try:
            response = lambda_handler(event, context)
            response_body = Json.loads(response['body'])

            self.assertIsInstance(response_body, list)
            self.assertEqual(len(response_body), len(ai_responses))
        except APIException as e:
            self.fail(f"lambda_handler raised APIException unexpectedly: {e}")

