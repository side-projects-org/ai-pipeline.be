import json
from unittest import TestCase

from pynamodb.exceptions import DoesNotExist

from api.sample.api_get_sample_model_by_key.api_get_sample_model_by_key import lambda_handler

class Test(TestCase):
    def test_lambda_handler_with_non_existent_key(self):
        event = {
            'queryStringParameters': {
                'key': 'non_existent_key'
            }
        }

        context = None

        response = lambda_handler(event, context)

        self.assertEqual(response['statusCode'], 404)

    def test_lambda_handler_with_existent_key(self):
        event = {
            'queryStringParameters': {
                'key': 'c6ed6a51-5381-4041-a146-a2f45592cbe0'
            }
        }

        context = None

        response = lambda_handler(event, context)

        self.assertEqual(response['statusCode'], 200)
        response_body = json.loads(response['body'])

        print(response_body)
