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
	# $(eval export VERSION=$$(cat VERSION))
	# echo ${VERSION}
	# $(eval export BRANCH=$(git branch | grep \* | cut -d ' ' -f2 | cut -d '/' -f2))
	# $(eval export FILTER="before=${REGISTRY_USERNAME}/${REGISTRY_IMAGE_NAME}:$$VERSION-$(BRANCH)")
	# $(eval export IMAGES=`docker images --filter='$$FILTER'  | awk '/^*cluster*/ {print $3}'`)
	# docker rmi $(IMAGES);
	# docker rmi $(docker images --filter='before=davidevitelaru/clustermanager:0.1.0.36-docker'  | awk '/^*cluster*/ {print $3}')

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

image: increment_build
	@docker build . -t ${REGISTRY_USERNAME}/${REGISTRY_IMAGE_NAME}:`cat VERSION`-${BRANCH}

run_image: image
	@if [[ "`docker ps | grep clustermanager`" != "" ]]; then docker stop clustermanager; fi;
	@if [[ "`docker ps -a | grep clustermanager`" != "" ]]; then docker rm clustermanager; fi;
	@docker run --name clustermanager -d ${REGISTRY_USERNAME}/${REGISTRY_IMAGE_NAME}:`cat VERSION`-${BRANCH} > /dev/null 2>1

publish: image
	@docker push ${REGISTRY_USERNAME}/${REGISTRY_IMAGE_NAME}:`cat VERSION`-${BRANCH}
