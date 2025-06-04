import unittest
import uuid
from unittest.mock import Mock
from warnings import deprecated

from api.prompt.api_put_prompt_model.api_put_prompt_model import lambda_handler
from common.Json import Json
from common.dynamodb.model import M


class TestApiPutPromptModelWithoutMocking(unittest.TestCase):
    @unittest.skip("This test code not working, must have refactoring")
    def test_lambda_handler_valid_input(self):
        # Real input data
        random_version = str(uuid.uuid4())
        event = {
            "body": Json.dumps({
                "prompt_name": "test_prompt",
                "version": random_version,
                "model": "GPT-4",
                "messages": [{"role": "user", "content": "Hello"}],
                "temperature": 0.7,
                "max_completion_tokens": 100,
            })
        }
        context = {}

        # mocking the response for testing purposes
        M.Prompt.get_item = Mock(return_value=M.Prompt(
            prompt_name="test_prompt",
            version=random_version,
            params={
                "model": "GPT-4",
                "temperature": 0.7,
                "max_completion_tokens": 100,
                "messages": [{"role": "user", "content": "Hello"}]
            }
        ))
        # Call the lambda handler
        response = lambda_handler(event, context)
        body = Json.loads(response["body"])


        print(response)
        # Assertions
        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(body["prompt_name"], "test_prompt")
        self.assertEqual(body["version"], random_version)
        self.assertEqual(body["params"]["model"], "GPT-4")
        self.assertEqual(body["params"]["temperature"], 0.7)
        self.assertEqual(body["params"]["max_completion_tokens"], 100)

if __name__ == "__main__":
    unittest.main()