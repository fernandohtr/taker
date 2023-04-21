install:
	pip install -r src/taker/requirements/base.txt -r src/api/requirements/base.txt

install-dev:
	pip install -r src/taker/requirements/dev.txt -r src/api/requirements/dev.txt

start:
	docker-compose -f docker/docker-compose.yml up -d

stop:
	docker-compose -f docker/docker-compose.yml down

logs:
	docker-compose -f docker/docker-compose.yml logs -f

clean-cache:
	docker exec messeger redis-cli -n 0 FLUSHALL

test-taker:
	PYTHONPATH=src/taker pytest src/taker/tests

test-api:
	PYTHONPATH=src/api pytest src/api/tests

test: test-taker test-api
