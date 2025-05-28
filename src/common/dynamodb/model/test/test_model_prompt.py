import unittest

from common.dynamodb.model import M


class TestModelPrompt(unittest.TestCase):
    def test_model_prompt(self):
        # Test the model prompt functionality
        prompt = M.Prompt.get('f35219e2-874b-4e8d-b736-65435634525f')

        json_data = prompt.to_simple_dict()
        serialize = prompt.serialize()
        data = prompt.attribute_values
        data['params'] = data['params'].attribute_values
        simple_dict = prompt.to_simple_dict()


