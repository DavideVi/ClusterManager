'''
Polling is handled externally by calling this script
This script will output the required information ONCE and append timestamps
'''
import os, boto3, time, datetime
from inventory_manager import InventoryManager
from models import Instance, InstanceRecord
from mongoengine import DoesNotExist

'''
Checking if database information is present in order to use the database
If information is not present the application will simply output to the terminal
'''
USE_DB = True

if 'CM_DB_URI' not in os.environ:
    print("\033[93mExport CM_DB_URI as the database url in order to save to database")
    print("Example: '$ export CM_DB_URI=\"mongodb://localhost\"\033[0m'")
    USE_DB = False

if 'CM_DB_NAME' not in os.environ:
    print("\033[93mExport CM_DB_NAME as the database name in order to save to database")
    print("Example: '$ export CM_DB_NAME=\"clustermanager\"'\033[0m")
    USE_DB = False

if not USE_DB:
    print("\033[93mWarning: Database will not be used\033[0m")

def main():

    session = boto3.Session() # will be created with EC2 role
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    inventory_manager = InventoryManager(session)
    inventory = inventory_manager.list_inventory()

    for item in inventory:
        # Using \t as a delimiter in case of awk
        print (timestamp + "\t" + item["name"] + "\t" + item["type"] + "\t" + item["zone"])

        if USE_DB:
            instance = None
            # Retrieving the instance if it exists
            try:
                instance = Instance.objects.get(instance_id = item["id"])
            # Creating the instance if it doesn't
            except DoesNotExist:
                instance = Instance(
                    instance_id = item["id"],
                    instance_name = item["name"],
                    instance_type = item["type"],
                    instance_zone = item["zone"],
                    instance_account = item["account"]
                )

            instance.records.append(InstanceRecord(
                timestamp = timestamp,
                instance_state = item["state"]
            ))

            instance.save()

if __name__ == '__main__':
    main()
