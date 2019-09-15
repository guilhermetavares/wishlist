build:
	docker-compose build

test: ## Run all tests (pytest).
	@echo "--> Testing on Docker."
	docker-compose run --rm test py.test $(path) -s --cov-report term --cov-report html
