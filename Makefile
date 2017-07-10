SHELL:=/bin/bash

define USAGE
Commands:
	make tests	- Runs tests
	make server	- Starts the server
	make query_aws	- Only starts the polling script
	make run_image	- Builds and runs the application in a container
	make publish	- Pushes the image to DockerHub
endef

export USAGE
export CM_DB_URI=mongodb://localhost
export CM_DB_NAME=inventory_manager
export REGISTRY_USERNAME=davidevitelaru
export REGISTRY_IMAGE_NAME=clustermanager
export BRANCH=$(shell git branch | grep \* | cut -d ' ' -f2 | cut -d '/' -f2)
export CURRENT_VERSION=$(shell cat VERSION)
export PREVIOUS_IMAGES=$(shell docker images --filter='before=${REGISTRY_USERNAME}/${REGISTRY_IMAGE_NAME}:${CURRENT_VERSION}-${BRANCH}'  | awk '/^*cluster*/ {print $$3}')

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
	-docker rmi ${PREVIOUS_IMAGES}

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
	@perl -i -pe 's/\b(\d+)(?=\D*$$)/$$1+1/e' VERSION

update_compose_version:
	sed -i.bak 's/davidevitelaru\/clustermanager:.*/davidevitelaru\/clustermanager:${CURRENT_VERSION}-${BRANCH}"/' docker-compose.yaml

image: increment_build
	@docker build . -t ${REGISTRY_USERNAME}/${REGISTRY_IMAGE_NAME}:`cat VERSION`-${BRANCH}

run_image: image
	@if [[ "`docker ps | grep clustermanager`" != "" ]]; then docker stop clustermanager; fi;
	@if [[ "`docker ps -a | grep clustermanager`" != "" ]]; then docker rm clustermanager; fi;
	@docker run --name clustermanager -d ${REGISTRY_USERNAME}/${REGISTRY_IMAGE_NAME}:`cat VERSION`-${BRANCH} > /dev/null

publish: image
	@docker push ${REGISTRY_USERNAME}/${REGISTRY_IMAGE_NAME}:`cat VERSION`-${BRANCH}
