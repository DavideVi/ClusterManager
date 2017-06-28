'''
Polling is handled externally by calling this script
This script will output the required information ONCE and append timestamps
'''
import os
from inventory_manager import InventoryManager

def main():



    session = create_session()
    inventory_manager = InventoryManager()

'''
Creates a boto3 session using the given execution role
'''
def create_session(self, execution_role):

    sts_client = boto3.client('sts')
    assumedRoleObject = sts_client.assume_role(
        RoleArn=execution_role,
        RoleSessionName="AssumeRoleSession"
    )
    credentials = assumedRoleObject['Credentials']
    boto3_session = boto3.Session( aws_access_key_id = credentials['AccessKeyId'],
        aws_secret_access_key = credentials['SecretAccessKey'],
        aws_session_token = credentials['SessionToken']
        )

    return boto3_session

if __name__ == '__main__':
    main()
