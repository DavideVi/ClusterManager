'''
Polling is handled externally by calling this script
This script will output the required information ONCE and append timestamps
'''
import os, boto3, time, datetime
from inventory_manager import InventoryManager

def main():
    session = boto3.Session() # will be created with EC2 role
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    inventory_manager = InventoryManager(session)
    inventory = inventory_manager.list_inventory()

    for item in inventory:
        # Using \t as a delimiter in case of awk
        print (timestamp + "\t" + item["name"] + "\t" + item["type"] + "\t" + item["region"])

if __name__ == '__main__':
    main()
