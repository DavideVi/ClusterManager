# Inventory Polling Script

## Deployment

Requirements:
+ EC2 instance
    * Ubuntu distribution
        - Python 2.7.*
        - Python pip
    * An IAM role must be associated with the instance and must have the following permissions:
        - EC2 DescribeInstances
        - STS GetCallerIdentity
+ A MongoDB database
    * I've attempted to deploy a Mongo container using Ansible - but the docker module was broken by its dependencies being made backwards-incompatible. Will fix in a later iteration.
    * If a database exists (can be easily set up `docker run --name some-mongo -p 27017:27017 -d mongo`), the app can be pointed to it by exporting the `CM_DB_URI` and `CM_DB_NAME` variables.

Script is compatible with Python3 but Ansible cannot deploy it using a Python 3 interpreter. Username `ubuntu` is hard-coded.

To deploy:
```bash
# Archive the sources so that they can be uploaded
zip -r clustermanager.zip inventory_manager.py main.py models.py
# Run the playbook - Ensure that you specify your target hosts
ansible-playbook deploy.yaml --extra-vars "target=<your target hosts> db_uri=mongodb://<database location>/ db_name=<database name>"
```

## Architecture

### Application Structure
Application consists of:
* Class `InventoryManager` used as a wrapper for AWS API calls.
* Main script that requests the information using `InventoryManager`.
    - It is intended to be called on a regular basis from an external service (such as `cron`).
    - It outputs the results along with a timestamp.
* The database models
    - Used to map objects to database collections/tables
    - Connection to database is created based on the `CM_DB_URI` and `CM_DB_NAME` system environment variables
    - If variables are not present, no database connection will be attempted

The inventory logic has been placed in its own module (`inventory_manager.py`) so that it can be imported into any existing projects / frameworks. The main script in this case is just used to call the module and could easily be deployed as a Lambda.

The inventory logic, the class `InventoryManager`, is initialised with a boto3 session object so that the calls are made against a customisable account (specified in a main script).

The main script will pull credentials from the EC2 metadata. This is for good practice/security reasons as keys should not be present on instances.

The main script will check if the `CM_DB_URI` and `CM_DB_NAME` system variables are set. If they are not then warnings will be outputted to STDERR. The app can function without a database connection but will always output warnings.

If the system variables are set, then the database will be used and the main script will also write to the database in addition to STDOUT.

### Application Maintainability

Future features that can be added as their own modules that would be called from the main script. Feature that would retrieve data would be called first, features that would process the data would be called after.

In the event of a migration to a different platform (e.g. Lambda, Django), only the main script would require changes.

### Deployment Structure
Deployment is done using an Ansible playbook that does the following:
 - Installs the necessary dependencies.
 - Uploads the code contained in the archive `clustermanager.zip`.
 - Detects the region the EC2 instance is in using `ec2metadata` and sets the region in `~/.aws/config` so that the script may use it.
 - Extracts the sources and makes them executable.
 - Sets the system environment variables required for database connection.
 - Sets up a cron job that runs the script every hour and outputs stdout and stderr.

The polling period set as part of the cron job is 1 hour as that is the amount of billable time set by AWS. Terminated instances would also be recorded so it's unlikely anything will be missed if an instance is created and terminated within an hour.

**Note:** Deployment paths are set to `/home/ubuntu` for simplicity. Ideally they would be deployed to `/usr/bin` and logs would go in `/var/log`. The application would also run as its own user that has limited access.

### Deployment Maintainability
The playbook would require changes in case additional services are required or if the cron command would need to change.

The instance IAM role policies would also need updating if additional AWS services are being used.

The update process is simplified with Ansible and takes less than a minute to complete. The transition to a new version is seamless if it happens between cron executions (which are one hour apart).

The database is non-relational and would not require any migrations - Thus future versions of the application could function with the same database.
