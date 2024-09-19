SHELL := /bin/bash

.PHONY: help
.DEFAULT_GOAL := help
.ONESHELL: # Applies to every target in the file https://www.gnu.org/software/make/manual/html_node/One-Shell.html
MAKEFLAGS += --silent # https://www.gnu.org/software/make/manual/html_node/Silent.html

help: ## 💬 Shows available commands
	grep -E '[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-23s\033[0m %s\n\n", $$1, $$2}'

setup-local-env: ## 🐍 Create a virtual environment and install dependencies
	@sh ./scripts/setup-local.sh

run-unit-tests: ## 🧪 Run unit tests
	@sh ./scripts/run-unit-tests.sh

run: ## 🚀 Run the application
	@sh ./scripts/run.sh $(ARGS)

run-help: ## 🚀 Run the application with help
	@sh ./scripts/run-help.sh