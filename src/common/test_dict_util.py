from unittest import TestCase

from common.dict_util import deep_update


class Test(TestCase):
    def test_deep_update(self):
        # Given
        dict1 = {
            "key1": "value1",
            "key2": {
                "key3": "value3",
                "key4": {
                    "key5": "value5"
                },
                "key8": 8
            }
        }
        dict2 = {
            "key2": {
                "key4": {
                    "key5": "changed",
                    "key6": "value6"
                },
                "key7": 7
            }
        }

        # When
        deep_update(dict1, dict2)

        # Then
        expected_dict = {
            "key1": "value1",
            "key2": {
                "key3": "value3",
                "key4": {
                    "key5": "changed",
                    "key6": "value6"
                },
                "key7": 7,
                "key8": 8
            }
        }
        self.assertDictEqual(dict1, expected_dict)


