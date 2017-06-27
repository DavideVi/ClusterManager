# Requirements

* Poll AWS and return the current EC2 cloud inventory. Log it, or print it to the console.
* Create a minimal deployment script which allows us to deploy this App to an AWS EC2 instance.
* Write a short description of:
 - The architecture of your App and how it supports adding future features.
 - Architectural changes you will have to make to your App to supports adding future features.
* Write a short description of:
 - Any improvements to your deployment script/process to enable seemless upgrades, and service reliability.

## Feature 1
Save the inventory returned from polling the polling inventory of EC2 instances to a database.

## Feature 2
Create an API to query which returns inventory information:
* the latest aggregate information
  - by region/zone
  - by instance type
* a time series of aggregate information
  - by region/zone
  - by instance type
* detailed information of instances for any point in time

## Feature 3
Create an API which which returns you EC2 cost information:
* the latest aggregate information
  - by region/zone
  - by instance type
* a time series of aggregate information
  - by region/zone
  - by instance type
