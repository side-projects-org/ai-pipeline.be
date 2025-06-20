import unittest
from unittest import TestCase

from api.ai_response.api_delete_ai_response.api_delete_ai_response import validate_request_body, lambda_handler
from common import APIException, ErrorCode
from common.Json import Json
from common.dynamodb.attributes import Attr, AiMessageAttribute
from common.dynamodb.model import M


class Test(TestCase):

    def test_validate_request_body(self):
        query_params = {
            'prompt_name': 'test_prompt',
            'version': '1.0',
            'key': 'EW256F4-3D2A-4B1C-8A2B-1C2D3E4F5G6H',
        }

        validate_request_body(query_params)

        self.assertEqual(1, 1)

    def test_validate_request_body_missing(self):
        query_params = {
            'prompt_name': 'test_prompt',
        }

        with self.assertRaises(APIException) as context:
            validate_request_body(query_params)

        self.assertEqual(context.exception.error_code, ErrorCode.INVALID_PARAMETER)
        missing_fields = context.exception.kwargs['param']

        self.assertTrue('key' in missing_fields)
        self.assertTrue('version' in missing_fields)


    def test_lambda_handler(self):
        # given
        ai_response = M.AiResponse(
            prompt_name='test_prompt',
            version='1.0',
            key='EW256F4-3D2A-4B1C-8A2B-1C2D3E4F5G6H',
            params=Attr.AiRequestParamsAttribute(
                messages=[
                    AiMessageAttribute(role="assistant", content="I'm fine, thank you!")
                ],
                model="gpt-3.5-turbo",
                temperature=0.7,
                max_completion_tokens=150
            ),
            answer=Attr.AnswerAttribute(
                id="response_id_123",
                object="chat.completion",
                created=1696156800,
                model="gpt-3.5-turbo",
                choices=[
                    Attr.ChoiceAttribute(
                        index=0,
                        message=Attr.AiMessageAttribute(
                            role="assistant",
                            content="I'm fine, thank you!"
                        ),
                        finish_reason="stop"
                    )
                ])
        )

        ai_response.save()

        body = {
            'prompt_name': ai_response.prompt_name,
            'version': ai_response.version,
            'key': ai_response.key
        }

        event = {
            'body': Json.dumps(body),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
        # when
        response = lambda_handler(event, None)
        res_body = Json.loads(response['body'])

        deleted = M.AiResponse.get_item(
            prompt_name=ai_response.prompt_name,
            version=ai_response.version,
            key=ai_response.key
        )

        # then
        self.assertTrue('message' in res_body)
        self.assertEqual(res_body['message'], 'deleted')
        self.assertIsNone(deleted)

