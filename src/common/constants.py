import os
import logging


logger = logging.getLogger("common.constants")


def get_env(env_name, filename, default='not-assigned'):
    env = os.environ.get(env_name, default)

    if env == default:
        file = os.path.join(os.path.dirname(__file__), filename)
        file = os.path.abspath(file)
        # 파일이 있는 경우에만 읽어서 업데이트하도록 수정
        if os.path.exists(file):
            f = open(file, "r")
            env = f.read().strip().strip("\"")
            f.close()
        else:
            logger.error(f"ENV '{env_name}' not setting. Check the file or environment variable.\n"
                         f"Searching File Path: {file}")

    return env


class BaseConfig:
    AWS_REGION = 'ap-northeast-2'

    PROJECT_NAME = get_env('PROJECT_NAME', '../../project_env/live/project_name.txt')
    STAGE_NAME = get_env('STAGE_NAME', '../../project_env/live/stage_name.txt')
    OPEN_AI_KEY = get_env('OPEN_AI_KEY', '../../project_env/live/open_ai_key.txt')
