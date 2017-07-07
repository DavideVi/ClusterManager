from itertools import chain

AWS_REGIONS = [
    'us-east-2',
    'us-east-1',
    'us-west-1',
    'us-west-2',
    'ca-central-1',
    'ap-south-1',
    'ap-northeast-2',
    'ap-southeast-1',
    'ap-southeast-2',
    'ap-northeast-1',
    'eu-central-1',
    'eu-west-1',
    'eu-west-2',
    'sa-east-1'
]


class InventoryManager():

    def __init__(self, boto3_session):
        self.session = boto3_session
        self.account = self.session.client('sts').get_caller_identity().get('Account')

    def list_inventory(self):
        clients = [
            self.session.client('ec2', region_name=region_name)
            for region_name in AWS_REGIONS
        ]

        raw_inventory = list(chain([
            client.describe_instances()
            for client in clients
        ]))

        return [
            # All keys are mandatory, if one of them is missing
            # the application will crash, but we'd have bigger problems
            {
                'name': self.get_name(instance),
                'id': instance["InstanceId"],
                'type': instance["InstanceType"],
                'state': instance["State"]["Name"],
                'region': instance["Placement"]["AvailabilityZone"],
                'zone': instance["Placement"]["AvailabilityZone"],
                'account': self.account
            }
            for reservations in raw_inventory
            for reservation in reservations["Reservations"]
            for instance in reservation["Instances"]
        ]

    def get_name(self, instance):
        """
        Return an instance's name.

        Default value is '<Nameless> to makes output easier
        to process or query
        """
        for tag in instance.get("Tags", []):
            if tag["Key"] == "Name":
                return tag["Value"]

        return "<Nameless>"
