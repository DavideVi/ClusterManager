SHELL:=/bin/bash

define USAGE
Commands:
	make tests
	make server
	make query_aws
	make image
endef

export USAGE
export CM_DB_URI=mongodb://localhost
export CM_DB_NAME=inventory_manager
export REGISTRY_USERNAME=davidevitelaru
export REGISTRY_IMAGE_NAME=clustermanager
export BRANCH=`git branch | grep \* | cut -d ' ' -f2 | cut -d '/' -f2`

usage:
	@echo "$$USAGE"

clean:
	@printf "Cleaning repo:\n"
	echo "${PATH}"
	rm -rf \
		*.egg-info \
		dist/ \
		build/ \
		cover \
		.coverage \
		unit.xml
	find . -name '*.pyc' -exec rm {} +

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

increment_build:
	perl -i -pe 's/\b(\d+)(?=\D*$$)/$$1+1/e' VERSION

image: increment_build
	@docker build . -t ${REGISTRY_USERNAME}/${REGISTRY_IMAGE_NAME}:`cat VERSION`-${BRANCH}

publish: image
	@docker push ${REGISTRY_USERNAME}/${REGISTRY_IMAGE_NAME}:`cat VERSION`-${BRANCH}
