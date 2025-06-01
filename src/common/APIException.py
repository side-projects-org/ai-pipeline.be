import traceback

from common.ErrorCode import ErrorCode
from common.Json import Json


class APIException(Exception):
    def __init__(self, error_code: ErrorCode, **kwargs):
        self.error_code = error_code
        self.status_code = error_code.status_code
        self.kwargs = kwargs

        try:
            self.message = error_code.client_message_template.format(**kwargs)
        except KeyError as e:
            self.message = f"[템플릿 오류] {e} 키 누락"

        try:
            self.server_log = error_code.server_log_template.format(**kwargs)
        except KeyError as e:
            self.server_log = f"[서버로그 템플릿 오류] {e} 키 누락"

        super().__init__(self.message)


    def build_aws_response(self):
        body = {
            "message": self.message,
            "traceback": traceback.format_exception_only(type(self), self)
        }

        return {
            "statusCode": self.status_code,
            "headers": {
                "Content-Type": "application/json",
            },
            "isBase64Encoded": False,
            "body": Json.dumps(body)
        }