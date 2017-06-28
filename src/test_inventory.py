import unittest, boto3, placebo
from os import listdir
from os.path import isfile, join
from inventory import InventoryManager

DATA_PATH = './mock_responses'

class TestInventoryManager(unittest.TestCase):

    '''
    Note: When playing back calls, placebo will start
    from 1 for each individual test
    '''
    def setUp(self):
        self.session = boto3.Session(
            aws_access_key_id="responses_will_be_mocked",
            aws_secret_access_key="responses_will_be_mocked"
        )
        pill = placebo.attach(self.session, data_path=DATA_PATH)
        pill.playback()

    '''
    Constructor must work
    '''
    def test_create(self):
        inventory_manager = InventoryManager(self.session)

    '''
    Listing inventory must work
    '''
    def test_list_inventory(self):
        inventory_manager = InventoryManager(self.session)
        result = inventory_manager.list_inventory()

    '''
    Listing inventory must return an array of instances containing:
        Instance name
        Instance ID
        Instance type
        Instance state
        Region it's running in
        Accoutn it's running in
    '''
    def test_list_inventory_result(self):

        inventory_manager = InventoryManager(self.session)

        # Running tests against all mock responses
        # Placebo handles this automatically but number of tests to run
        # depends on the number of 'DescribeInstances' responses we have
        mock_response_files = [f for f in listdir(DATA_PATH) if isfile(join(DATA_PATH, f))]
        for response_file in mock_response_files:
            if 'DescribeInstances' in response_file:

                result = inventory_manager.list_inventory()

                for instance_info in result:
                    self.assertIn('name', instance_info)
                    self.assertIn('id', instance_info)
                    self.assertIn('type', instance_info)
                    self.assertIn('state', instance_info)
                    self.assertIn('region', instance_info)
                    self.assertIn('account', instance_info)




if __name__ == '__main__':
    unittest.main()
