from common import ErrorCode


class APIException(Exception):
    """
    example:
     - raise APIException(APIErrorCode.INVALID_PARAMETER)
     - raise APIException(APIErrorCode.INVALID_PARAMETER, 'Invalid parameter')
     - raise APIException(APIErrorCode.INVALID_PARAMETER, 'Invalid parameter', 400)
    """

    def __init__(self, error_code: ErrorCode, message: str = None, status_code=400):
        self.error_code = error_code
        self.message = message if message else error_code.client_message
        self.status_code = status_code if status_code else error_code.status_code
        super().__init__(self.message)

    def __dict__(self):
        return {
            'message': self.message,
            'status_code': self.status_code,
        }
