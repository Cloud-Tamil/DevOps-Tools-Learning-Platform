.PHONY: help venv install test scan sonar-up sonar-down ci clean

help:
	@echo "make venv       - create virtualenv"
	@echo "make install    - install deps"
	@echo "make test       - run tests with coverage"
	@echo "make sonar-up   - start SonarQube + PostgreSQL"
	@echo "make sonar-down - stop SonarQube"
	@echo "make scan       - run sonar-scanner (needs SONAR_TOKEN)"
	@echo "make ci         - test + scan with quality gate wait"
	@echo "make clean      - remove build artifacts"

venv:
	python3 -m venv .venv
	@echo "Run: source .venv/bin/activate"

install:
	pip install --upgrade pip
	pip install -r requirements.txt

test:
	pytest --cov=src --cov-report=term --cov-report=xml:coverage.xml

sonar-up:
	docker compose up -d
	@echo "SonarQube: http://localhost:9000 (admin/admin)"

sonar-down:
	docker compose down

scan:
	@test -n "$(SONAR_TOKEN)" || (echo "SONAR_TOKEN not set" && exit 1)
	sonar-scanner \
		-Dsonar.host.url=http://localhost:9000 \
		-Dsonar.token=$(SONAR_TOKEN)

ci: test
	@test -n "$(SONAR_TOKEN)" || (echo "SONAR_TOKEN not set" && exit 1)
	sonar-scanner \
		-Dsonar.host.url=http://localhost:9000 \
		-Dsonar.token=$(SONAR_TOKEN) \
		-Dsonar.qualitygate.wait=true

clean:
	rm -rf .pytest_cache .coverage coverage.xml htmlcov .scannerwork
	find . -name __pycache__ -type d -exec rm -rf {} +
