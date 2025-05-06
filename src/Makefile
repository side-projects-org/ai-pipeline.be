.PHONY: all zip-all clean-all diff-all

ZIP_TARGET_DIRS := \
	common \
	$(shell find api -mindepth 2 -maxdepth 2 -type d -name "api_*") \
	layer \
	worker

EXCLUDE_PATTERNS := \
	-name "*.zip" -o \
	-name "*.sha" -o \
	-name "*.tmp" -o \
	-name "*.bak" -o \
	-path "*/code/*" -o \
	-path "*/__pycache__/*" -o \
	-name "Makefile*"


all: zip-all

# TODO layer build 는 zip-all 에서 제외해야 함 (docker 통해서 빌드해야함)
zip-all:
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