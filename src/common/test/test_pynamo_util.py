import datetime
import json
import unittest
import uuid
import logging


from common.dynamodb.model import SampleModel
from common.pynamo_util import model_to_dict

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class TestPynamoUtil(unittest.TestCase):
    def test_get_pynamodb_model_to_dict(self):
        # Given
        # uuid_key = uuid.uuid4().__str__()
        now = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
        given_dict = {
            'key': uuid.uuid4().__str__(),
            'unicode_attr': 'unicode_attr',
            'bool_attr': True,
            'num_attr': 1,
            'utc_datetime_attr': now,
            'ttl_attr': now.replace(microsecond=0),
            # 'unicode_set_attr': {'a', 'b'},
            # 'num_set_attr': {1, 2},
            'list_attr': [1, 'a', True],
            'list_attr_fix_object_type': [{'attr1': 'a', 'attr2': 'b'}],
            'list_attr_fix_primitive_type': [1, 2, 3],
            'dynamic_map_attr': {'unknown_attr': 'a', 'unknown_attr2': 'b'},
            'custom_map_attr': {'attr1': 'a', 'attr2': 'b'},
            'custom_dynamic_map_attr': {'attr1': 'a', 'attr2': 'b', 'attr3': 'c'},
            'gsi_partition_key': 'gsi_partition_key',
            'gsi_sort_key': 'gsi_sort_key',
            'custom_wrapping_dynamic_map_attr': {'attr1': 'a', 'attr2': 'b', 'unknown_attr': 'c'}
        }

        sample = SampleModel(**given_dict)
        sample.save()

        # read_sample = SampleModel.get(uuid_key)

        result_dict = model_to_dict(sample)

        # get cost time
        start = datetime.datetime.now()

        for i in range(1000):
            result_dict = model_to_dict(sample)

        end = datetime.datetime.now()
        print("cost time: ", (end - start).total_seconds(), "s")
        print(json.dumps(result_dict, indent=4, default=str))

        for k, expect in given_dict.items():
            actual = result_dict[k]
            self.assertEqual(expect, actual)

        sample.delete()
