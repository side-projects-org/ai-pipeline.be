.PHONY: python_env_init
python_env_init:
	@if [ -d "src/.venv" ]; then \
		echo "\033[33mVirtual environment already exists in src folder.\033[0m"; \
		exit 0; \
	else \
		echo "Creating virtual environment in src folder..."; \
		cd src && python3.12 -m venv .venv && source .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt; \
		echo "Done."; \
	fi

# boilerplate 이므로, 새로운 remote에 연결하기 위해 기존 remote를 제거합니다.
.PHONY: remove_origin
remove_origin:
	@if git config --get remote.origin.url > /dev/null; then \
		echo "Current origin: $$(git remote get-url origin)"; \
		echo "Removing origin..."; \
		git remote remove origin; \
		echo "Done."; \
	else \
		echo "\033[33mNo origin found.\033[0m"; \
	fi
