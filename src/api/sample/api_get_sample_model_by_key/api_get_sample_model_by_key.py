from http import HTTPStatus

from pynamodb.exceptions import DoesNotExist

from common import APIException, ErrorCode
from common.pynamo_util import model_to_dict
from common.dynamodb.model import M

from common.awslambda.response_handler import ResponseHandler


@ResponseHandler.api
def lambda_handler(event, context):
    # QUERY PARAMETER 에서 key 를 꺼내온다.
    if 'queryStringParameters' not in event or 'key' not in event['queryStringParameters']:
        exc = Exception('there is no required parameters')
        setattr(exc, 'status_code', HTTPStatus.BAD_REQUEST)
        raise exc

    key = event['queryStringParameters']['key']

    try:
        sample = M.Sample.get(key)
    except DoesNotExist as e:
        raise APIException(ErrorCode.DYNAMO_ITEM_NOT_FOUND, key=key)

    return sample.to_simple_dict()
