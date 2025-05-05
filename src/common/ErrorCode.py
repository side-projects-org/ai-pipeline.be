from enum import Enum

class ErrorCode(Enum):
    INVALID_PARAMETER = (
        400,
        "요청 파라미터가 잘못되었습니다: {param}",
        "잘못된 파라미터 입력: {param}"
    )
    RESOURCE_NOT_FOUND = (
        404,
        "{resource}을(를) 찾을 수 없습니다.",
        "존재하지 않는 {resource} 요청"
    )
    INTERNAL_ERROR = (
        500,
        "서버 오류가 발생했습니다.",
        "예기치 못한 서버 오류 발생: {detail}"
    )

    def __init__(self, status_code: int, client_template: str, server_template: str):
        self.status_code = status_code
        self.client_message_template = client_template
        self.server_log_template = server_template