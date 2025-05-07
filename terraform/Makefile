ROOT_DIR := ".."
$(eval export TF_VAR_projectName := $(shell cat ${ROOT_DIR}/project_env/live/project_name.txt || tr A-Z a-z))
$(eval export TF_VAR_stage := $(shell cat ${ROOT_DIR}/project_env/live/stage_name.txt || tr A-Z a-z))


plan:
	terraform plan

apply:
	terraform apply

destroy:
	terraform destroyye