# Inventory Polling Script

## Deployment

Requirements:
* EC2 instance
 * Ubuntu distribution
   - Python 2.7.*
   - Python pip
 * An IAM role must be associated with the instance and must have the following permissions:
   - EC2 DescribeInstances
   - STS GetCallerIdentity

Script is compatible with Python3 but Ansible cannot deploy it using a Python 3 interpreter. Username `ubuntu` is hard-coded.

To deploy:
```bash
# Archive the sources so that they can be uploaded
zip -r clustermanager.zip inventory_manager.py main.py
# Run the playbook - Ensure that you specify your target hosts
ansible-playbook deploy.yaml --extra-vars "target=<your target hosts>"
```

## Architecture

### Application Structure
Application consists of:
 - Class `InventoryManager` used as a wrapper for AWS API calls.
 - Main script that requests the information using `InventoryManager`.
  - It is intended to be called on a regular basis from an external service (such as `cron`).
  - It outputs the results along with a timestamp.

The inventory logic has been placed in its own module (`inventory_manager.py`) so that it can be imported into any existing projects / frameworks. The main script in this case is just used to call the module and could easily be deployed as a Lambda.

The inventory logic, the class `InventoryManager`, is initialised with a boto3 session object so that the calls are made against a customisable account (specified in a main script).

The main script will pull credentials from the EC2 metadata. This is for good practice/security reasons as keys should not be present on instances.

### Application Maintainability

Future features that can be added as their own modules that would be called from the main script. Feature that would retrieve data would be called first, features that would process the data would be called after.

In the event of a migration to a different platform (e.g. Lambda, Django), only the main script would require changes.

### Deployment Structure
Deployment is done using an Ansible playbook that does the following:
 - Installs the necessary dependencies.
 - Uploads the code contained in the archive `clustermanager.zip`.
 - Detects the region the EC2 instance is in using `ec2metadata` and sets the region in `~/.aws/config` so that the script may use it.
 - Extracts the sources and makes them executable.
 - Sets up a cron job that runs the script every hour and outputs stdout and stderr.

The polling period set as part of the cron job is 1 hour as that is the amount of billable time set by AWS. Terminated instances would also be recorded so it's unlikely anything will be missed if an instance is created and terminated within an hour.

**Note:** Deployment paths are set to `/home/ubuntu` for simplicity. Ideally they would be deployed to `/usr/bin` and logs would go in `/var/log`. The application would also run as its own user that has limited access.

### Deployment Maintainability
The playbook would require changes in case additional services are required (e.g. a database that would have to be either deployed or pointed to) or if the cron command would need to change.

The instance IAM role policies would also need updating if additional AWS services are being used.
