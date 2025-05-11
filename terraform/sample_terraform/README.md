# 설명
실행하면, 기본 인프라 구조 만들어짐 (lambda, layer, api gateway, dynamodb)

## 실행 환경
- AWS CLI 설치되어 있어, aws configure 되어있다고 가정(해당 설정으로 aws 접근하게 됨)
- 윈도우 환경이더라도, wsl(ubuntu) 사용
## 변수 설정
- terraform.tfvars 파일 만들어서 그 안에 환경변수 설정해두면 자동 로드되어 실행됨
  - projectName ="dlsj"
    stage = "lsj2"
  - 위처럼 쓰면 된다~
- 또는 TF_VAR_환경변수 선언 필요! (<-Makefile에 정의되어있음)
- **DB정상 연결 확인을 위해선, SampleModel에 DB 이름 바꿀 것!!!**
## 실행
- makefile 복사해서 수정하여 넣어놨으나, 정상실행여부 확인 못함
- 정상 실행 안된다면 커맨드에서 아래 명령어 실행
1. `cd terraform/sample_terraform`
2. `terraform init`
3. `terraform plan`
4. `terraform apply`