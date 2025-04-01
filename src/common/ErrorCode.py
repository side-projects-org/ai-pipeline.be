class ErrorCode:
    def __init__(self, code: str, client_message: str, server_message: str):
        self.status_code = code
        self.client_message = client_message
        self.server_message = server_message

    def to_client_dict(self):
        return {
            'status_code': self.status_code,
            'client_message': self.client_message,
        }

    def __str__(self):
        return 'ErrorCode: {0} - {1}'.format(self.status_code, self.server_message)


ErrorCode.BAD_REQUEST = ErrorCode('400', 'Bad Request', 'The request is invalid or malformed.')
ErrorCode.UNAUTHORIZED = ErrorCode('401', 'Unauthorized','The request has not been applied because it lacks valid authentication credentials for the target resource.')
ErrorCode.FORBIDDEN = ErrorCode('403', 'Forbidden', 'The server understood the request, but is refusing to fulfill it.')
ErrorCode.NOT_FOUND = ErrorCode('404', 'Not Found', 'The server has not found anything matching the Request-URI.')
