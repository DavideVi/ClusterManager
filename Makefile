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

image: info
	set -ex
	# SET THE FOLLOWING VARIABLES
	# docker hub username
	USERNAME=davidevitelaru
	# image name
	IMAGE=clustermanager
	# ensure we're up to date
	git pull
	# bump version
	docker run --rm -v "$PWD":/app treeder/bump patch
	version=`cat VERSION`
	echo "version: $version"
	# run build
	docker build -t $USERNAME/$IMAGE:latest .
	# tag it
	git add -A
	git commit -m "version $version"
	git tag -a "$version" -m "version $version"
	git push
	git push --tags
	docker tag $USERNAME/$IMAGE:latest $USERNAME/$IMAGE:$version
	# push it
	docker push $USERNAME/$IMAGE:latest
	docker push $USERNAME/$IMAGE:$version
