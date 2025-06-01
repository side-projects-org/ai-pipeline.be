import time
import unittest
import uuid

from common.dynamodb.model import M


class TestModelPrompt(unittest.TestCase):
    def test_model_prompt(self):
        # Test the model prompt functionality
        prompt_dict = {
            'prompt_name': 'test_prompt',
            'version': '1.0',
            'params': {
                'messages': [
                    {'role': 'user', 'content': 'Hello, how are you?'},
                    {'role': 'assistant', 'content': 'I am fine, thank you!'}
                ],
                'max_tokens': 100,
                'model': 'gpt-3.5-turbo',
                'response_format': 'text',
                'temperature': 0.7,
                'stream': False
            },
        }

        prompt = M.Prompt(**prompt_dict)
        prompt.save()

        self.assertEqual(prompt.prompt_name, 'test_prompt')

        prompt.delete()

    def test_model_query(self):
        prompt_name = str(uuid.uuid4())
        prompt_dict = {
            'prompt_name': prompt_name,
            'version': '1.0',
            'params': {
                'messages': [
                    {'role': 'user', 'content': 'Hello, how are you?'},
                    {'role': 'assistant', 'content': 'I am fine, thank you!'}
                ],
                'max_tokens': 100,
                'model': 'gpt-3.5-turbo',
                'response_format': 'text',
                'temperature': 0.7,
                'stream': False
            },
        }

        prompts = []
        for i in range(1, 20):
            prompt_dict['version'] = f'1.{i}'
            prompt = M.Prompt(**prompt_dict)
            prompt.save()
            prompts.append(prompt)


        queried_prompts = list(M.Prompt \
            .pk_prompt_name_sk_item_type__created_at_index \
            .query(hash_key=prompt_name))

        self.assertEqual(len(queried_prompts), 19)

        for i in range(len(queried_prompts)):
            queried_prompt = queried_prompts[i]
            actual_prompt = prompts[i]

            self.assertEqual(queried_prompt.prompt_name, actual_prompt.prompt_name)
            self.assertEqual(queried_prompt.version, actual_prompt.version)


        for prompt in prompts:
            prompt.delete()

