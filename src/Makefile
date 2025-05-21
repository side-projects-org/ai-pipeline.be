PROJECT_ROOT := $(shell pwd | sed 's|\(/src\).*|\1|')


.PHONY: all zip-all clean-all diff-all

ZIP_TARGET_DIRS := \
	$(shell find api -mindepth 2 -maxdepth 2 -type d -name "api_*") \
	$(shell find worker -mindepth 2 -maxdepth 2 -type d -name "worker_*")

ZIP_COMMON_SRC_TARGET_DIRS := common

ZIP_LIBRARY_LAYER_DIR := \
	$(shell find layer -mindepth 1 -maxdepth 1 -type d -name "layer_*")

EXCLUDE_PATTERNS := \
	-name "*.zip" -o \
	-name "*.sha" -o \
	-name "*.tmp" -o \
	-name "*.bak" -o \
	-name "*.md" -o \
	-name '.DS_Store' -o \
	-name "Makefile*" -o \
	-path "*/code/*" -o \
	-path "*__pycache__*" -o \
	-path "*python*"


setup:
	@echo "Setting up the environment..."; \
	python3 -m venv .venv; \
	source .venv/bin/activate; \
	pip install -r requirements.txt; \

clean-common-src:
clean-all:

common: zip-common-src-all

all: zip-src-all zip-layer-all zip-common-src-all

zip-layer-all:
	@for dir in $(ZIP_LIBRARY_LAYER_DIR); do \
		echo "\n📦 Zipping: $$dir"; \
		\
		BUILD_ZIP="$$dir/layer.zip"; \
		BUILD_SHA="$$dir/layer.sha"; \
		BUILD_TMP="$$dir/layer.sha.tmp"; \
		\
		shasum -a 256 $$dir/requirements.txt \
			| awk '{ print $$1 }'> $$BUILD_TMP; \
		\
		if [ -f $$BUILD_SHA ]; then \
			OLD=$$(cat $$BUILD_SHA); NEW=$$(cat $$BUILD_TMP); \
			if [ "$$OLD" = "$$NEW" ]; then \
				echo "⏸️  No changes. Skipping."; \
				rm -f $$BUILD_TMP; \
				continue; \
			fi; \
		fi; \
		\
		mv $$BUILD_TMP $$BUILD_SHA; \
		\
		rm -rf $$dir/package; \
		mkdir -p $$dir/package; \
	  	\
	  	echo "🐳 Installing packages in Docker..."; \
		docker run \
			-v ${PROJECT_ROOT}/$$dir:/var/task \
			-v ${PROJECT_ROOT}/$$dir/package:/opt \
			"public.ecr.aws/sam/build-python3.12:latest-arm64" \
			/bin/sh -c "\
				pip install -r requirements.txt -q -t /opt/python/lib/python3.12/site-packages && \
				echo '📦 Completed installing packages.' && \
				echo '⛔️ Removing boto3 and related packages (built-in in Lambda)...' && \
				rm -rf /opt/python/lib/python3.12/site-packages/boto3* \
					   /opt/python/lib/python3.12/site-packages/botocore* \
					   /opt/python/lib/python3.12/site-packages/s3transfer*"; \
		cd $$dir/package && zip -qr ../layer.zip python/*; \
		\
		rm -rf $$dir/package; \
	done


zip-common-src-all:
	@for dir in $(ZIP_COMMON_SRC_TARGET_DIRS); do \
		echo "\n📦 Zipping: $$dir"; \
		BUILD_ZIP="$$dir/layer.zip"; \
		BUILD_SHA="$$dir/layer.sha"; \
		BUILD_TMP="$$dir/layer.sha.tmp"; \
		\
		find $$dir -type f ! \( $(EXCLUDE_PATTERNS) \) -print0 \
			| xargs -0 shasum -a 256 \
			| awk '{ print $$1 }' \
			| shasum -a 256 \
			| awk '{ print $$1 }' > $$BUILD_TMP; \
		\
		if [ -f $$BUILD_SHA ]; then \
			OLD=$$(cat $$BUILD_SHA); NEW=$$(cat $$BUILD_TMP); \
			if [ "$$OLD" = "$$NEW" ]; then \
				echo "⏸️  No changes. Skipping."; \
				rm -f $$BUILD_TMP; \
				continue; \
			fi; \
		fi; \
		\
		mv $$BUILD_TMP $$BUILD_SHA; \
		\
		rm -rf python; \
		mkdir python; \
		cp -r $$dir python/; \
		\
		zip -r $$BUILD_ZIP python/ \
			-x "*/code/*" "*/__pycache__/*" "*.zip" "*.sha" "*.tmp" "*.bak" "*DS_Store*" \
			-x "*/python*"; \
		echo "✅ Zipped $$dir → $$BUILD_ZIP"; \
		\
		rm -rf python; \
	done


zip-src-all:
	@for dir in $(ZIP_TARGET_DIRS); do \
		echo "\n📦 Zipping: $$dir"; \
		BUILD_ZIP="$$dir/build.zip"; \
		BUILD_SHA="$$dir/build.sha"; \
		BUILD_TMP="$$dir/build.sha.tmp"; \
		\
		find $$dir -type f ! \( $(EXCLUDE_PATTERNS) \) -print0 \
			| xargs -0 shasum -a 256 \
			| awk '{ print $$1 }' \
			| shasum -a 256 \
			| awk '{ print $$1 }' > $$BUILD_TMP; \
		\
		if [ -f $$BUILD_SHA ]; then \
			OLD=$$(cat $$BUILD_SHA); NEW=$$(cat $$BUILD_TMP); \
			if [ "$$OLD" = "$$NEW" ]; then \
				echo "⏸️  No changes. Skipping."; \
				rm -f $$BUILD_TMP; \
				continue; \
			fi; \
		fi; \
		mv $$BUILD_TMP $$BUILD_SHA; \
		zip -r $$BUILD_ZIP $$dir \
			-x "*/code/*" "*/__pycache__/*" "*.zip" "*.sha" "*.tmp" "*.bak"; \
		echo "✅ Zipped $$dir → $$BUILD_ZIP"; \
	done

clean-all: clean-src clean-layer clean-common-src

clean-src:
	@for dir in $(ZIP_TARGET_DIRS); do \
		echo "🧹 Cleaning: $$dir"; \
		rm -f $$dir/build.zip $$dir/build.sha $$dir/build.sha.tmp; \
	done
clean-layer:
	@for dir in $(ZIP_LIBRARY_LAYER_DIR); do \
		echo "🧹 Cleaning: $$dir"; \
		rm -f $$dir/layer.zip $$dir/layer.sha $$dir/layer.sha.tmp; \
		rm -rf $$dir/package; \
	done
clean-common-src:
	@for dir in $(ZIP_COMMON_SRC_TARGET_DIRS); do \
		echo "🧹 Cleaning: $$dir"; \
		rm -f $$dir/layer.zip $$dir/layer.sha $$dir/layer.sha.tmp; \
		rm -rf $$dir/package; \
	done



diff-all:
	@for dir in $(ZIP_TARGET_DIRS); do \
		BUILD_SHA="$$dir/build.sha"; \
		BUILD_TMP="$$dir/build.sha.tmp"; \
		\
		find $$dir -type f ! \( $(EXCLUDE_PATTERNS) \) -print0 \
			| xargs -0 shasum -a 256 \
			| awk '{ print $$1 }' \
			| shasum -a 256 \
			| awk '{ print $$1 }' > $$BUILD_TMP; \
		\
		if [ -f $$BUILD_SHA ]; then \
			OLD=$$(cat $$BUILD_SHA); NEW=$$(cat $$BUILD_TMP); \
			if [ "$$OLD" != "$$NEW" ]; then \
				echo "🟡 Changed: $$dir"; \
			else \
				echo "🟢 No change: $$dir"; \
			fi; \
		else \
			echo "🆕 No SHA yet: $$dir"; \
		fi; \
		rm -f $$BUILD_TMP; \
	done

.PHONY: api

api:
	@if [ -z "$(name)" ]; then \
		echo "❌ Error: missing 'name'. Usage: make api name=ACTION [domain=DOMAIN]"; \
		echo "EXAMPLE_1: make api name=api_get_sample_model_by_key "; \
		echo "EXAMPLE_2: make api name=api_get_sample_model_by_key domain=sample"; \
		exit 1; \
	fi; \
	domain=$${domain:-sample}; \
	path="api/$$domain/$(name)"; \
	file="$$path/$(name).py"; \
	template="lambda_handler_template.py"; \
	\
	mkdir -p "$$path"; \
	if [ ! -f "$$file" ]; then \
		cp $$template "$$file"; \
		echo "✅ Created: $$file with Lambda handler template"; \
	else \
		echo "⚠️ File already exists: $$file (skipped)"; \
	fi
