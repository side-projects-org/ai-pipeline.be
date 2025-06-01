import unittest
import uuid

from api.prompt.api_put_prompt_model.api_put_prompt_model import lambda_handler
from common.Json import Json


class TestApiPutPromptModelWithoutMocking(unittest.TestCase):
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