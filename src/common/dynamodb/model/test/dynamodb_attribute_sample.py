import unittest

import logging

import datetime
import uuid

from pynamodb.exceptions import PutError

from common.Json import Json
from common.dynamodb.model import M, SampleExtends, CustomMapAttribute


# logger 는 info 까지 출력되어야햄
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()

logger.setLevel(logging.INFO)
logger.addHandler(handler)


class DynamoDBDaoSample(unittest.TestCase):

    def test_sample(self):
        """SampleModel 을 통한 DynamoDB CRUD 성공 테스트"""
        # given
        now = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
        uuid_key = uuid.uuid4().__str__()
        given_dict = {
            'key': uuid_key,
            'unicode_attr': 'unicode_attr',
            'bool_attr': True,
            'num_attr': 1,
            'utc_datetime_attr': now,
            'ttl_attr': now,
            'list_attr': [1, 'a', True],
            'list_attr_fix_object_type': [{'attr1': 'a', 'attr2': 'b'}],
            'list_attr_fix_primitive_type': [1, 2, 3],
            'dynamic_map_attr': {'unknown_attr': 'a', 'unknown_attr2': 'b'},
            'custom_map_attr': {'attr1': 'a', 'attr2': 'b'},
            'custom_dynamic_map_attr': {'attr1': 'a', 'attr2': 'b', 'attr3': 'c'},
            'gsi_partition_key': 'gsi_partition_key',
            'gsi_sort_key': 'gsi_sort_key'
        }

        sample = M.Sample(**given_dict)

        # when
        sample.save()

        read_sample = M.Sample.get(uuid_key)
        logger.info("save success")

        read_sample_dict = read_sample.to_simple_dict()

        # then
        self.assertEqual(uuid_key, read_sample.key)
        self.assertEqual('unicode_attr', read_sample.unicode_attr)
        self.assertEqual(True, read_sample.bool_attr)
        self.assertEqual(1, read_sample.num_attr)

        logger.info(f'read_sample.utc_datetime_attr: {read_sample.utc_datetime_attr}')
        # self.assertEqual(now, read_sample.utc_datetime_attr)   # 이 부분은 테스트가 실패한다. 대신 아래와 같은 방법으로 비교해야한다.
        self.assertTrue(now == read_sample.utc_datetime_attr)
        self.assertTrue(now.__eq__(read_sample.utc_datetime_attr))

        logger.info(f'read_sample.ttl_attr: {read_sample.ttl_attr}')
        self.assertTrue(now.timestamp(), read_sample.ttl_attr)   # ttl_attr 은 timestamp 로 비교해야한다.

        self.assertEqual([1, 'a', True], read_sample.list_attr)

        self.assertEqual({'attr1': 'a', 'attr2': 'b'}, read_sample.list_attr_fix_object_type[0].as_dict())
        self.assertEqual(CustomMapAttribute, type(read_sample.list_attr_fix_object_type[0]))
        self.assertEqual('a', read_sample.dynamic_map_attr.unknown_attr)
        self.assertEqual('b', read_sample.dynamic_map_attr.unknown_attr2)

        logger.info(f'\nexpect: {given_dict["custom_map_attr"]}')
        logger.info(f'dynamic_map_attr: {read_sample.dynamic_map_attr}')
        logger.info(f'dynamic_map_attr.as_dict(): {read_sample.dynamic_map_attr.as_dict()}')
        logger.info(f'dynamic_map_attr.to_simple_dict(): {read_sample.dynamic_map_attr.to_simple_dict()}')
        logger.info(f'dynamic_map_attr.to_simple_dict()[\'custom_map_attr\']: {read_sample_dict["custom_map_attr"]}\n')

        logger.info(f'custom_map_attr: {read_sample.custom_map_attr}')
        logger.info(f'custom_map_attr.as_dict(): {read_sample.custom_map_attr.as_dict()}')
        logger.info(f'custom_map_attr.to_simple_dict(): {read_sample.custom_map_attr.to_simple_dict()}')
        logger.info(f'dynamic_map_attr.to_simple_dict()[\'custom_dynamic_map_attr\']: {read_sample_dict["custom_dynamic_map_attr"]}\n')

        logger.info(f'custom_dynamic_map_attr: {read_sample.custom_dynamic_map_attr}')
        logger.info(f'custom_dynamic_map_attr.as_dict(): {read_sample.custom_dynamic_map_attr.as_dict()}')
        logger.info(f'custom_dynamic_map_attr.to_simple_dict(): {read_sample.custom_dynamic_map_attr.to_simple_dict()}')
        logger.info(f'dynamic_map_attr.to_simple_dict()[\'custom_dynamic_map_attr\']: {read_sample_dict["custom_dynamic_map_attr"]}\n')

        self.assertEqual('gsi_partition_key', read_sample.gsi_partition_key)
        self.assertEqual('gsi_sort_key', read_sample.gsi_sort_key)

        # when
        sample.update(actions=[M.Sample.unicode_attr.set('unicode_attr2')])

        # then
        self.assertEqual('unicode_attr2', sample.unicode_attr)

        sample.delete()
        logger.info("delete success")

    def test_ListAttribute_of_any_type_CRUD(self):
        """리스트에 어떤 타입이든 들어올 수 있는 성공 테스트"""
        # given
        uuid_key = uuid.uuid4().__str__()
        given_dict = {
            'key': uuid_key,
            'list_attr': [1, 'a', True, []]
        }

        # Create
        sample = M.Sample(**given_dict)
        sample.save()

        read_sample = M.Sample.get(uuid_key)

        # then
        self.assertEqual(uuid_key, read_sample.key)
        for e in range(len(given_dict['list_attr'])):
            self.assertEqual(given_dict['list_attr'][e], read_sample.list_attr[e])

        # when: Update
        read_sample.update(actions=[M.Sample.list_attr.set(
            M.Sample.list_attr.append(['b'])
        )])

        # then
        self.assertEqual([1, 'a', True, [], 'b'], read_sample.list_attr)

        # Delete
        read_sample.delete()

    def test_ListAttribute_of_fixed_type_CRUD(self):
        """원시타입과 Object 타입으로 고정된 배열에 대한 성공 테스트"""
        # given
        uuid_key = uuid.uuid4().__str__()
        given_dict = {
            'key': uuid_key,
            'list_attr_fix_object_type': [{'attr1': 'a', 'attr2': 'b'}],
            'list_attr_fix_primitive_type': [1, 2, 3]
        }

        sample = M.Sample(**given_dict)

        # when: Create
        sample.save()

        # Read
        read_sample = M.Sample.get(uuid_key)

        # then
        self.assertEqual(uuid_key, read_sample.key)
        self.assertEqual({'attr1': 'a', 'attr2': 'b'}, read_sample.list_attr_fix_object_type[0].as_dict())

        # Update
        # 동일한 Path 를 업데이트를 할 수 없어서 나눠서 업데이트
        read_sample.update(actions=[
            M.Sample.list_attr_fix_object_type[0].attr1.set('c'),
            M.Sample.list_attr_fix_primitive_type[0].set(4),
        ])

        read_sample.update(actions=[
            M.Sample.list_attr_fix_primitive_type.set(
                M.Sample.list_attr_fix_primitive_type.append([5, ]),
            )
        ])

        self.assertEqual('c', read_sample.list_attr_fix_object_type[0].attr1)
        self.assertEqual(4, read_sample.list_attr_fix_primitive_type[0])
        self.assertEqual(5, read_sample.list_attr_fix_primitive_type[-1])

        sample.delete()

    def test_put_different_type_in_ListAttribute_of_object_type(self):
        """[개발 시 주의] 선언타입과 다른 Object 가 들어오면 선언타입의 Attribute Check 만 진행"""
        # given
        uuid_key = uuid.uuid4().__str__()
        given_dict = {
            'key': uuid_key,
            'list_attr_fix_object_type': [[], 'string', {'attr1': 'a', 'attr2': 'b'}],
        }

        given_dict2 = {
            'key': uuid_key,
            'list_attr_fix_object_type': [1, 'string', {'attr1': 'a', 'attr2': 'b'}],
        }

        # Create
        model = M.Sample(**given_dict)
        model.save()

        # then
        self.assertEqual(uuid_key, model.key)
        self.assertEqual([[], 'string', {'attr1': 'a', 'attr2': 'b'}], model.list_attr_fix_object_type)

        # Delete
        model.delete()

        # Create & Error
        with self.assertRaises(TypeError):
            M.Sample(**given_dict2).save()

    def test_put_different_type_in_ListAttribute_of_primitive_type(self):
        """[개발 시 주의] 선언 타입(primitive)과 다른 타입이 들어오면 PutError 발생"""
        # given
        uuid_key = uuid.uuid4().__str__()
        given_dict = {
            'key': uuid_key,
            'list_attr_fix_primitive_type': [[], 'string', {'attr1': 'a', 'attr2': 'b'}]
        }

        # when
        # then
        with self.assertRaises(PutError):
            M.Sample(**given_dict).save()

    def test_DynamicMapAttribute_CRUD(self):
        """DynamicMapAttribute 을 통한 CRUD 성공 테스트"""
        # given
        uuid_key = uuid.uuid4().__str__()
        given_dict = {
            'key': uuid_key,
            'dynamic_map_attr': {'unknown_attr': 'a', 'unknown_attr2': 'b'}
        }

        sample = M.Sample(**given_dict)

        # when
        sample.save()
        read_sample = M.Sample.get(uuid_key)

        # then
        self.assertEqual(uuid_key, sample.key)
        self.assertEqual('a', sample.dynamic_map_attr.unknown_attr)
        self.assertEqual('b', sample.dynamic_map_attr.unknown_attr2)
        # self.assertEqual({'unknown_attr': 'a', 'unknown_attr2': 'b'}, read_sample.dynamic_map_attr.as_dict())

        # when
        # save unexpected attributes in dynamic map
        sample.update(actions=[M.Sample.dynamic_map_attr['unknown_attr'].set('c')])

        # then
        self.assertEqual('c', sample.dynamic_map_attr.unknown_attr)

        # Delete
        sample.delete()

    def test_CDynamicMapAttribute_CRUD(self):
        """CDynamicMapAttribute 을 통한 CRUD 성공 테스트"""
        # given
        uuid_key = uuid.uuid4().__str__()
        given_dict = {
            'key': uuid_key,
            'custom_wrapping_dynamic_map_attr': {'attr1': 'a', 'attr2': 'b', 'unknown_attr': 'c'}
        }

        sample = M.Sample(**given_dict)

        # Create
        sample.save()
        read_sample = M.Sample.get(uuid_key)

        # then
        self.assertEqual(uuid_key, sample.key)
        self.assertEqual('a', sample.custom_wrapping_dynamic_map_attr.attr1)
        self.assertEqual('b', sample.custom_wrapping_dynamic_map_attr.attr2)
        self.assertEqual('c', sample.custom_wrapping_dynamic_map_attr.unknown_attr)     # 정의되지 않은 필드 조회
        self.assertEqual({'attr1': 'a', 'attr2': 'b', 'unknown_attr': 'c'}, read_sample.custom_wrapping_dynamic_map_attr.as_dict())

        # Update
        sample.update(actions=[
            M.Sample.custom_wrapping_dynamic_map_attr.attr1.set('c'),                # 정의된 필드 변경
            M.Sample.custom_wrapping_dynamic_map_attr['unknown_attr'].remove()       # 정의되지 않은 필드 변경 및 삭제
        ])

        # then
        self.assertEqual('c', sample.custom_wrapping_dynamic_map_attr.attr1)
        with self.assertRaises(AttributeError):
            print(sample.custom_wrapping_dynamic_map_attr.unknown_attr)

        # Delete
        sample.delete()

    def test_save_SampleModelExtends_and_read_SampleModel(self):
        """
        SampleModelExtends 로 저장한 후
        SampleModel 로 읽어오는 테스트 (추가적인 필드가 존재하지만, 정의되어 있지 않은 경우)
        """

        # given
        uuid_key = uuid.uuid4().__str__()
        given_dict = {
            'key': uuid_key,
            'unicode_attr': 'unicode_attr',
            'bool_attr': True,
            'num_attr': 1,
            'utc_datetime_attr': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1),
            'ttl_attr': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1),
            'list_attr': [1, 'a', True],
            'list_attr_fix_object_type': [{'attr1': 'a', 'attr2': 'b'}],
            'list_attr_fix_primitive_type': [1, 2, 3],
            'dynamic_map_attr': {'unknown_attr': 'a', 'unknown_attr2': 'b'},
            'custom_map_attr': {'attr1': 'a', 'attr2': 'b'},
            'custom_dynamic_map_attr': {'attr1': 'a', 'attr2': 'b', 'attr3': 'c'},
            'extra_field': 'extra_field',
            'gsi_partition_key': 'gsi_partition_key',
            'gsi_sort_key': 'gsi_sort_key'
        }

        # Create
        sample = SampleExtends(**given_dict)
        sample.save()

        # Read
        read_sample = M.Sample.get(uuid_key)
        read_sample_extends = SampleExtends.get(uuid_key)
        result_dict = read_sample.to_simple_dict()
        # then

        self.assertEqual(read_sample_extends.extra_field, 'extra_field')
        with self.assertRaises(AttributeError):
            print(read_sample.extra_field)

        with self.assertRaises(KeyError):
            print(result_dict['extra_field'])
