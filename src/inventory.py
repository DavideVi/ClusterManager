import boto3

class InventoryManager():

    def __init__(self, boto3_session):
        self.session = boto3_session

    def list_inventory(self):
        ec2 = self.session.client('ec2')
        return ec2.describe_instances()
        # self.session.client('sts').get_caller_identity().get('Account')
