from enum import Enum

class ErrorCode(Enum):
    PARAMETER_NOT_FOUND = (
        400,
        "요청 파라미터가 없습니다: {param}",
        "파라미터 없음: {param}"
    )
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
    DYNAMO_ITEM_NOT_FOUND = (
        404,
        "DynamoDB에서 항목을 찾을 수 없습니다 [search key: {key}]",
        "DynamoDB 항목 없음: [search key: {key}]"
    )
    DYNAMO_EXCEPTION = (
        500,
        "DynamoDB 작업 중 오류가 발생했습니다: {detail}",
        "DynamoDB 작업 오류: {detail}"
    )

    def __init__(self, status_code: int, client_template: str, server_template: str):
        self.status_code = status_code
        self.client_message_template = client_template
        self.server_log_template = server_template