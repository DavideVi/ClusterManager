# Architecture

## Overall Structure

### Core Inventory Logic

The core inventory logic will call the right AWS APIs and retrieve the desired information.

Core inventory logic will be in its own package.
 - Easier to plug in to any framework (Lamda/Flask/Django)
 - Logic is separated

Core inventory logic needs to be polled.Different approaches are possible:
 - Lambda with CloudWatch event + data stored in CloudWatch logs or directly in database.
 - Standalone app executed with cron.

Requirement stated that it has to be deployed to an EC2 instance, so the second approach will be followed. Migration is always possible and would require less effort to implement than the initial solution.

The application could easily be dockerised and deployed into an existing swarm or on a fresh instance.

### Database Choice
In terms of database, a non-relational database will be used, namely MongoDB. Because it is non-relational, it will make migrations easier in the long term (if we ever want to store more data regarding an instance). The type of data that is stored also makes a non-relational a better option.

Disadvantages include deployment and backing up as we do not have the convenience of an RDS instance. DynamoDB could be used instead, but in case cloud providers would ever have to be switched, migration would be more difficult with DynamoDB than with most AWS services (In terms of time required to perform the migration of both data and code makes use it).

The read/write logic will be wrapped in its own package - this simplifies development and maintanance as the developer would not need to be aware of the 'schema'.
