from http import HTTPStatus

from common import model_to_dict
from common.dynamodb.model import SampleModel

from common.awslambda import ResponseHandler


@ResponseHandler.api
def lambda_handler(event, context):
    # QUERY PARAMETER 에서 key 를 꺼내온다.
    if 'queryStringParameters' not in event or 'key' not in event['queryStringParameters']:
        exc = Exception('there is no required parameters')
        setattr(exc, 'status_code', HTTPStatus.BAD_REQUEST)
        raise exc

    key = event['queryStringParameters']['key']

    sample = SampleModel.get(key)

    if sample is None:
        exc = Exception(f'there is no such data [key={key}]')
        setattr(exc, 'status_code', HTTPStatus.NOT_FOUND)
        raise exc

    return model_to_dict(sample)
