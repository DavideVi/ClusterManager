import boto3

class InventoryManager():

    def __init__(self, boto3_session):
        self.session = boto3_session
        self.account = self.session.client('sts').get_caller_identity().get('Account')

    def list_inventory(self):

        ec2 = self.session.client('ec2')
        raw_inventory = ec2.describe_instances()

        inventory = []

        for reservation in raw_inventory["Reservations"]:
            for instance in reservation["Instances"]:

                instance_name = ""

                # Extracting name
                if "Tags" in instance:
                    for tag in instance["Tags"]:
                        if tag["Key"] == "Name":
                            instance_name = tag["Value"]
                            break

                # All keys are mandatory, if one of them is missing
                # the application will crash, but we'd have bigger problems
                inventory.append({
                    'name': instance_name,
                    'id': instance["InstanceId"],
                    'type': instance["InstanceType"],
                    'state': instance["State"]["Name"],
                    'region': instance["Placement"]["AvailabilityZone"],
                    'account': self.account
                })

        return inventory
