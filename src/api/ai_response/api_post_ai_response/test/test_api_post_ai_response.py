import unittest
from unittest import TestCase

from api.ai_response.api_post_ai_response.api_post_ai_response import validate_request_body, save_ai_response
from common import APIException, ErrorCode
from common.dynamodb.attributes import Attr
from common.dynamodb.model import M


class Test(TestCase):
    def test_validate_request_body_no_params(self):
        body = {
            "prompt_name": "test_prompt",
            # "version": "1.0",
            "response": {
                "id": "response123",
                "choices": [
                    {"text": "This is a test response."}
                ],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 20,
                    "total_tokens": 30
                },
                "object": "test_object",
                "created": 1234567890
            }
        }

        with self.assertRaises(APIException) as context:
            validate_request_body(body)

        self.assertEqual(context.exception.error_code, ErrorCode.INVALID_PARAMETER)


    def test_validate_request_body(self):
        body = {
            "prompt_name": "test_prompt",
            "prompt_version": "1.0",
            "response": {
                "id": "response123",
                "choices": [
                    {"text": "This is a test response."}
                ],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 20,
                    "total_tokens": 30
                },
                "object": "test_object",
                "created": 1234567890
            }
        }

        try:
            validate_request_body(body)
        except APIException as e:
            self.fail(f"validate_request_body raised APIException unexpectedly: {e}")


    def test_save_ai_response(self):
        prompt = M.Prompt(
            prompt_name="test_prompt",
            version="1.0",
            params=Attr.AIRequestParamsAttribute(
                model="gpt-3.5-turbo",
                temperature=0.7,
                max_completion_tokens=150,
                messages=[Attr.AIMessageAttribute(role="user", content="Hello, how are you?")]
            )
        )

        body = {
            "prompt_name": "test_prompt",
            "version": "1.0",
            "response": {
                "id": "response123",
                "choices": [
                    {"text": "This is a test response."}
                ],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 20,
                    "total_tokens": 30
                },
                "object": "test_object",
                "created": 1234567890
            }
        }
        ai_response = None
        try:
            ai_response = save_ai_response(body, prompt)

            self.assertIsNotNone(ai_response)

            self.assertEqual(ai_response.prompt_name, body["prompt_name"])
            self.assertEqual(ai_response.version, body["version"])

            self.assertEqual(ai_response.response.id, body["response"]["id"])

            print("AIResponse saved successfully:", ai_response.to_simple_dict())
        except Exception as e:
            self.fail(f"save_ai_response raised an exception unexpectedly: {e}")
        finally:
            if ai_response is not None:
                ai_response.delete()

# Run tests
if __name__ == "__main__":
    unittest.main()