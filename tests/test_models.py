import unittest, os
from mongoengine import *

# Database environment variables need exporting before
# importing the models. Do not change the order of these lines.
os.environ['CM_DB_URI'] = 'mongodb://localhost'
os.environ['CM_DB_NAME'] = 'test_db'
from models import Instance, InstanceRecord

class TestInstance(unittest.TestCase):

    '''
    Clearing up the test database before each execution
    '''
    def setUp(self):
        Instance.drop_collection()

    '''
    Ensuring that we can create and retrieve an instance
    '''
    def test_instance(self):

        instance = Instance(
            instance_id = "TestID",
            instance_name = "TestName",
            instance_type = "TestType",
            instance_zone = "TestZone",
            instance_account = "TestAccount"
            )
        instance.save()

        query_result = Instance.objects(instance_id = "TestID")

        # Only one item should have been inserted
        self.assertEquals(1, query_result.count())
        # The only item should be identical to the one we've inserted
        self.assertEquals(instance, query_result[0])

    '''
    No insertion should happen unless all required fields have been specified
    '''
    def test_required(self):

        # ID is mandatory
        instance = Instance(
            instance_name = "TestName",
            instance_type = "TestType",
            instance_zone = "TestZone",
            instance_account = "TestAccount"
            )
        with self.assertRaises(ValidationError) as ve:
            instance.save()

        # Type is mandatory
        instance = Instance(
            instance_id = "TestID",
            instance_name = "TestName",
            instance_zone = "TestZone",
            instance_account = "TestAccount"
            )
        with self.assertRaises(ValidationError) as ve:
            instance.save()

        # Zone is mandatory
        instance = Instance(
            instance_id = "TestID",
            instance_name = "TestName",
            instance_type = "TestType",
            instance_account = "TestAccount"
            )
        with self.assertRaises(ValidationError) as ve:
            instance.save()

        # Account is mandatory
        instance = Instance(
            instance_id = "TestID",
            instance_name = "TestName",
            instance_type = "TestType",
            instance_zone = "TestZone"
            )
        with self.assertRaises(ValidationError) as ve:
            instance.save()

        # Name is not mandatory
        instance = Instance(
            instance_id = "TestID",
            instance_type = "TestType",
            instance_zone = "TestZone",
            instance_account = "TestAccount"
            )
        instance.save()

    '''
    No two instances should have the same ID
    '''
    def test_instance_duplicate(self):
        instance = Instance(
            instance_id = "TestID",
            instance_name = "TestName",
            instance_type = "TestType",
            instance_zone = "TestZone",
            instance_account = "TestAccount"
            )
        instance.save()

    def test_instance_record_save(self):

        # Attempting to add record before saving
        record_1 = InstanceRecord(
            instance_state = "RUNNING"
        )

        instance_1 = Instance(
            instance_id = "TestID",
            instance_name = "TestName",
            instance_type = "TestType",
            instance_zone = "TestZone",
            instance_account = "TestAccount",
            records = [record_1]
            )

        instance_1.save()

        query_result = Instance.objects(records__instance_state="RUNNING")
        self.assertEquals(1, query_result.count())
        self.assertEquals(instance_1, query_result[0])

        # Attempting to add record after saving
        instance_2 = Instance(
            instance_id = "TestID2",
            instance_name = "TestName",
            instance_type = "TestType",
            instance_zone = "TestZone",
            instance_account = "TestAccount",
            )
        instance_2.save()

        record_2 = InstanceRecord(
            instance_state = "TERMINATED"
        )
        instance_2.records.append(record_2)
        instance_2.save()

        query_result = Instance.objects(records__instance_state="TERMINATED")
        self.assertEquals(1, query_result.count())
        self.assertEquals(instance_2, query_result[0])





if __name__ == '__main__':
    unittest.main()
