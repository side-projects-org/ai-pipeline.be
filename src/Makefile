PROJECT_ROOT := $(shell pwd | sed 's|\(/src\).*|\1|')


.PHONY: all zip-all clean-all diff-all

ZIP_TARGET_DIRS := \
	common \
	$(shell find api -mindepth 2 -maxdepth 2 -type d -name "api_*") \
	$(shell find worker -mindepth 2 -maxdepth 2 -type d -name "worker_*")

# TODO common 분리하기

ZIP_LIBRARY_LAYER_DIR := \
	$(shell find layer -mindepth 1 -maxdepth 1 -type d -name "layer_*")

EXCLUDE_PATTERNS := \
	-name "*.zip" -o \
	-name "*.sha" -o \
	-name "*.tmp" -o \
	-name "*.bak" -o \
	-name "*.md" -o \
	-name "Makefile*" -o \
	-path "*/code/*" -o \
	-path "*/__pycache__/*"



all: zip-src-all zip-layer-all

zip-layer-all:
	@for dir in $(ZIP_LIBRARY_LAYER_DIR); do \
		echo "\n📦 Zipping: $$dir"; \
		\
		BUILD_ZIP="$$dir/build.zip"; \
		BUILD_SHA="$$dir/build.sha"; \
		BUILD_TMP="$$dir/build.sha.tmp"; \
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
		cd $$dir/package && zip -qr ../build.zip python/*; \
		\
		rm -rf $$dir/package; \
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

clean-all:
	@for dir in $(ZIP_TARGET_DIRS); do \
		echo "🧹 Cleaning: $$dir"; \
		rm -f $$dir/build.zip $$dir/build.sha $$dir/build.sha.tmp; \
	done

	@for dir in $(ZIP_LIBRARY_LAYER_DIR); do \
		echo "🧹 Cleaning: $$dir"; \
		rm -f $$dir/build.zip $$dir/build.sha $$dir/build.sha.tmp; \
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