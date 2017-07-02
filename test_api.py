import unittest, os, datetime
from server import app

# Database environment variables need exporting before
# importing the models. Do not change the order of these lines.
os.environ['CM_DB_URI'] = 'mongodb://localhost'
os.environ['CM_DB_NAME'] = 'test_db'
from models import Instance, InstanceRecord

class TestAPIMethods(unittest.TestCase):

    '''
    Setting up the test data
    '''
    @classmethod
    def setUpClass(self):
        # Creating a test client for Flask
        self.app = app.test_client()
        self.app.testing = True

        # Clearing test DB
        Instance.drop_collection()

        # Setting up 60 instances
        create = {
            "eu-west-1a": {
                "t2.micro": 5,
                "t2.nano": 20
            },
            "eu-west-1b": {
                "t2.micro": 8,
                "m4.xlarge": 7
            },
            "eu-west-1c": {
                "t2.micro": 9
            },
            "eu-west-2a": {
                "t2.micro": 11
            }
        }

        instance_id_counter = 0
        for zone in create:
            for itype in create[zone]:
                for count in range(0,create[zone][itype]):
                    instance = Instance(
                        instance_type = itype,
                        instance_id = "i-" + str(instance_id_counter),
                        instance_zone = zone,
                        instance_account = "testaccount"
                    )
                    instance.save()
                    instance_id_counter += 1

        # Spreading instance records across 12 months
        timestamps = []
        for i in range(-12,0):
            timestamps.append(monthdelta(datetime.datetime.now(), i))

    def setUp(self):
        pass

    '''
    Should return total number of servers per region and instance type
    '''
    def test_aggregate(self):

        response = self.app.get('/aggregate')

        self.assertEqual('Hello', response.data)

    def test_aggregate_region(self):
        pass

    def test_aggregate_type(self):
        pass

'''
Helper method to substract months
Source: https://stackoverflow.com/questions/3424899/whats-the-simplest-way-to-subtract-a-month-from-a-date-in-python
'''
def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)

if __name__ == '__main__':
    unittest.main()
