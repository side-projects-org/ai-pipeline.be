# Python Project Boilerplate

## Tech Stack
- Lang : Python 3
- DB   : DynamoDB
- Infra: AWS Lambda, API Gateway, SQS, S3, DynamoDB
- CI/CD: Terraform, Github Actions, Makefile
- IDE  : PyCharm
- Test : unittest
- Lib
  - PynamoDB : DynamoDB ORM
  - firebase-admin : Firebase Admin SDK
  - boto3 : AWS SDK
  - requests : HTTP Request


## Project Structure

- /src
  - /api
  - /common
  - /worker
  - /layer
- /project_env
  - /live
  - /sample
- /terraform


## IDE Setting
IDE 가 PyCharm 인 경우, 
Preference > Project Structure 

1. 기존 root를 삭제
2. add content root를 눌러서 /src 폴더를 추가
3. /src 폴더를 마우스 우클릭 후 Mark Directory as > Sources Root 선택

