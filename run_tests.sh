export AWS_DEFAULT_REGION=us-east-1
nosetests \
    --with-coverage \
    --cover-package=inventory_manager \
    --cover-html \
    --cover-branches \
    --cover-min-percentage=80 \
    test_inventory_manager.py test_models.py
# python test_api.py
