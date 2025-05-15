from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, MapAttribute, ListAttribute, DynamicMapAttribute, BooleanAttribute, \
    NumberAttribute, UTCDateTimeAttribute, TTLAttribute

from common.constants import BaseConfig
from common.dynamodb.attributes.CustomAttribute import CDynamicMapAttribute


class SampleGlobalIndex(GlobalSecondaryIndex):
    class Meta:
        # required settings: index_name, projection
        index_name = "sample_global_index"
        projection = AllProjection()

    gsi_partition_key = UnicodeAttribute(hash_key=True)
    gsi_sort_key = UnicodeAttribute(range_key=True)


# 사전에 정의된 속성만을 허용한다.
class CustomMapAttribute(MapAttribute):
    attr1 = UnicodeAttribute(null=True)
    attr2 = UnicodeAttribute(null=True)


# 사전에 정의된 속성만을 허용한다.
class CustomDynamicMapAttribute(DynamicMapAttribute):
    attr1 = UnicodeAttribute(null=True)
    attr2 = UnicodeAttribute(null=True)


# 사전에 정의된 속성만을 허용한다.
class CustomMyDynamicMapAttribute(CDynamicMapAttribute):
    attr1 = UnicodeAttribute(null=True)
    attr2 = UnicodeAttribute(null=True)


class Sample(Model):
    key = UnicodeAttribute(hash_key=True)

    gsi_partition_key = UnicodeAttribute(null=True)
    gsi_sort_key = UnicodeAttribute(null=True)

    # 타입별로 정의
    unicode_attr: UnicodeAttribute = UnicodeAttribute(null=True)  # string
    bool_attr = BooleanAttribute(null=True)  # boolean
    num_attr = NumberAttribute(default=0)  # number
    utc_datetime_attr = UTCDateTimeAttribute(null=True)  # UTC datetime

    # 옵션 타입 (epoch time, 즉 숫자로 저장됩니다)
    # attributes 로 조회하는 경우, datetime.datetime 으로 변환된다
    ttl_attr = TTLAttribute(null=True)  # TTL

    # 리스트나 맵, 셋 같은 복합 타입
    # unicode_set_attr = UnicodeSetAttribute(null=True)  # set of string 사용에 주의가 필요하다
    # num_set_attr = NumberSetAttribute(null=True)  # set of number 사용에 주의가 필요하다

    list_attr = ListAttribute(null=True, default=list)  # any type
    list_attr_fix_object_type = ListAttribute(of=CustomMapAttribute, null=True)  # 다른 타입이 오면 에러
    list_attr_fix_primitive_type = ListAttribute(of=NumberAttribute, null=True)  # 다른 타입이 오면 에러

    # map_attr = MapAttribute()                 # MapAttribute 는 바로 사용하는 것이 권장되지 않는다
    dynamic_map_attr = DynamicMapAttribute(null=True)

    custom_map_attr = CustomMapAttribute(null=True)
    custom_dynamic_map_attr = CustomDynamicMapAttribute(null=True)

    custom_wrapping_dynamic_map_attr = CustomMyDynamicMapAttribute(null=True)

    # gsi
    sample_global_index = SampleGlobalIndex()

    class Meta:
        table_name = "dlsj-lsj2"
        region = BaseConfig.AWS_REGION


class SampleExtends(Sample):
    extra_field = UnicodeAttribute(null=True)
