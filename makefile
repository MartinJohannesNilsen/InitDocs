.PHONY: venv-setup install-build-deps install-deps wheel executable

# Define OSTYPE based on the operating system
ifeq ($(OS),Windows_NT)
	OSTYPE := Windows
else
	OSTYPE := $(shell uname 2>/dev/null || echo Unknown)
endif

venv-setup:
	@if [ ! -d ".venv" ]; then \
		echo "\n> Setting up venv"; \
		python3 -m venv .venv; \
	fi

install-deps: venv-setup
	@echo "\n> Installing project dependencies in virtual environment"
	@if [ "$(OSTYPE)" = "Windows" ]; then \
		.venv\Scripts\pip install -U pip; \
		.venv\Scripts\pip install .; \
	else \
		.venv/bin/pip install -U pip; \
		.venv/bin/pip install .; \
	fi

install-build-deps: install-deps
	@echo "\n> Installing build dependencies in virtual environment"
	@if [ "$(OSTYPE)" = "Windows" ]; then \
		.venv\Scripts\pip install --upgrade pip setuptools wheel; \
		.venv\Scripts\pip install --require-virtualenv ".[build]"; \
	else \
		.venv/bin/pip install --upgrade pip setuptools wheel; \
		.venv/bin/pip install --require-virtualenv ".[build]"; \
	fi

# Building the project wheel
wheel: install-build-deps
	@echo "\n> Building wheel"
ifeq ($(OSTYPE),Windows)
	.venv\Scripts\python -m build
else
	.venv/bin/python -m build
endif

# Packaging the project executable
executable: install-build-deps
	@echo "\n> Creating executable with PyInstaller"
ifeq ($(OSTYPE),Windows)
	.venv\Scripts\pyinstaller initdocs.spec
else
	.venv/bin/pyinstaller initdocs.spec
endif
