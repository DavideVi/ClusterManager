class InventoryManager():

    def __init__(self, boto3_session):
        self.session = boto3_session
        self.account = self.session.client('sts').get_caller_identity().get('Account')

    def list_inventory(self):
        ec2 = self.session.client('ec2')
        raw_inventory = ec2.describe_instances()

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
            for reservation in raw_inventory["Reservations"]
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
