define USAGE
Commands:
	make tests
	make server
	make query_aws
endef

export USAGE
export AWS_DEFAULT_REGION=us-east-1
export CM_DB_URI=mongodb://localhost
export CM_DB_NAME=inventory_manager

usage:
	@echo "$$USAGE"

info:
	@python --version
	@pip --version

tests: info
	@nosetests \
	    --with-coverage \
	    --cover-package=inventory_manager \
	    --cover-html \
	    --cover-branches \
	    --cover-min-percentage=80 \
	    tests/test_inventory_manager.py tests/test_models.py

mongodb:
	docker inspect some-mongo > /dev/null || \
	docker run --name some-mongo -p 27017:27017 -d mongo

server: info
	python server.py

query_aws: info
	python main.py

demo: info mongodb query_aws server
	@echo "Demo started"
	@echo "Open http://localhost:5000/aggregate"
