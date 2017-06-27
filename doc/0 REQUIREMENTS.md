# Raw Requirements

* Poll AWS and return the current EC2 cloud inventory. Log it, or print it to the console.
* Create a minimal deployment script which allows us to deploy this App to an AWS EC2 instance.
* Write a short description of:
 - The architecture of your App and how it supports adding future features.
 - Architectural changes you will have to make to your App to supports adding future features.
* Write a short description of:
 - Any improvements to your deployment script/process to enable seemless upgrades, and service reliability.

## Database
Save the inventory returned from polling the polling inventory of EC2 instances to a database.

## API Endpoint
Create an API to query which returns inventory information:
* the latest aggregate information
  - by region/zone
  - by instance type
* a time series of aggregate information
  - by region/zone
  - by instance type
* detailed information of instances for any point in time

## Cost Information
Create an API which which returns you EC2 cost information:
* the latest aggregate information
  - by region/zone
  - by instance type
* a time series of aggregate information
  - by region/zone
  - by instance type

# Refined Requirements

* As an administrator I would like to monitor the state of the cloud inventory over time.
* As an administrator I would like the script to be deployed automatically.
* As an administrator I would like the inventory state to be stored in a database.
* As an administrator I would like an API endpoint to serve the monitored data.
  - Should serve instance type + region
  - Should keep track of time (i.e. creation and deletion time)
    - Should be able to handle requests with time as a parameter
  - Any other information (i.e. should be customisable for future needs)
* As an administrator I would like to be aware of the cloud inventory cost.
  - By region and instance type
  - Should keep track of time
    - Should be able to handle requests with time as a parameter

## Questions + Assumptions

**Why *poll* AWS?**
Assuming historical information has to be available.

**How often to poll?**
Why not make it customisable?

**Is it necessary for it to be deployed to an instance?**
Lambdas are cool, but perhaps a regular application might help with maintainability and might provide more power.

**Why not just query AWS APIs?** Historical data is not provided by AWS (as far as I'm aware), and a wrapper can process the data and present it in a nicer way (Nobody will ever care about ALL the information returned from an `ec2.get_instances()` call).

**Does data have to be retrieved across several accounts?** Effort to make it work across accounts is minimal so might as well implement it. Only need to remember for the database if a relational one is used.
