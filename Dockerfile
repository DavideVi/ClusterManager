FROM python:2.7.13

WORKDIR /usr/src/app

# Installing dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Setting up application
COPY *.py ./
## Workaround for it not copying the directory for some reason
RUN mkdir ./inventory_manager
COPY inventory_manager/*.py ./inventory_manager/
COPY VERSION ./

# Setting up default DB connection variables
ENV CM_DB_URI=mongodb://localhost
ENV CM_DB_NAME=inventory_manager

# Exposing required ports
EXPOSE 5000

CMD [ "python", "server.py" ]
