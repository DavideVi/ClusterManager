import unittest, os, datetime, random, json
from datetime import timedelta
from server import app

# Database environment variables need exporting before
# importing the models. Do not change the order of these lines.
os.environ['CM_DB_URI'] = 'mongodb://localhost'
os.environ['CM_DB_NAME'] = 'test_db'
from models import Instance, InstanceRecord

# Keeping the same 'now' time so that DB queries won't be "1 month and 1 second"
# away from making it into the query
LOAD_TIME = datetime.datetime.now()

class TestAPIMethods(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        '''
        Creating a test client for Flask
        '''
        self.app = app.test_client()
        self.app.testing = True

        # Clearing test DB
        Instance.drop_collection()

        '''
        Populating database with random test data
        '''
        MAX_INSTANCES = 60
        self.zones = [ "eu-west-1a", "eu-west-1b", "eu-west-1c", "eu-west-2a"]
        self.types = [ "t2.micro", "t2.nano", "m4.xlarge" ]
        to_create = {}

        # Creating random information from sample regions and types
        for index in range(0, MAX_INSTANCES):

            random_zone = self.zones[random.randint(0, len(self.zones) - 1)]
            random_type = self.types[random.randint(0, len(self.types) - 1)]

            if random_zone not in to_create:
                to_create[random_zone] = {}

            if random_type not in to_create[random_zone]:
                to_create[random_zone][random_type] = 1
            else:
                to_create[random_zone][random_type] += 1

        # Writing instance records to database based on random information
        instance_id_counter = 0
        for zone in  to_create:
            for itype in  to_create[zone]:
                for count in range(0, to_create[zone][itype]):
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
        for i in range(-11,1):
            timestamps.append(monthdelta(LOAD_TIME, i))

        # Going through all instances and creating records between two
        # randomly-selected timestamps
        for instance in Instance.objects():
            start = random.randint(0, len(timestamps) - 2)
            end = random.randint(start + 1, len(timestamps) - 1)

            for timestamp_index in range(start, end + 1):
                instance.records.append(InstanceRecord(
                    timestamp = timestamps[timestamp_index],
                    instance_state = "RUNNING"
                ))
                instance.save()

    '''
    Should return total number of servers per region and instance type
    for the last day
    '''
    def test_aggregate(self):

        '''
        Calculating expected result
        '''
        results = Instance.objects(records__timestamp__gte=(LOAD_TIME - timedelta(days=1)))
        expected = {}

        for instance in results:
            # We have zone but we want region
            instance_region = instance["instance_zone"][:-1]
            if instance_region not in expected:
                expected[instance_region] = {}
            if instance["instance_type"] not in expected[instance_region]:
                expected[instance_region][instance["instance_type"]] = 1
            else:
                expected[instance_region][instance["instance_type"]] += 1

        '''
        Making call and validating output
        '''
        raw_response = self.app.get('/aggregate')
        response = json.loads(raw_response.data)

        for expected_region in expected:
            # Region must be present in response
            self.assertIn(expected_region, response)

            for itype in expected[expected_region]:
                # Instance type must be present in expected region
                self.assertIn(itype, response[expected_region])
                # Counts must match
                self.assertEquals(
                        expected[expected_region][itype],
                        response[expected_region][itype]
                    )

    '''
    Should return total number of servers a single region
    Should be grouped by instance type and aggregate for the last day
    '''
    def test_aggregate_region(self):

        '''
        Extracting regions from zones
        '''
        regions = []

        for zone in self.zones:
            if zone[:-1] not in regions:
                regions.append(zone[:-1])

        '''
        Testing against all regions
        '''
        for region in regions:
            '''
            Calculating expected result
            '''
            results = Instance.objects(
                    instance_zone__contains = region,
                    records__timestamp__gte=(LOAD_TIME - timedelta(days=1))
                )
            expected = {
                str(region): {}
            }

            for instance in results:
                if instance["instance_type"] not in expected[region]:
                    expected[region][instance["instance_type"]] = 1
                else:
                    expected[region][instance["instance_type"]] += 1

            '''
            Making call and validating output
            '''
            raw_response = self.app.get('/aggregate/' + region)
            response = json.loads(raw_response.data)

            # Region must be present in response
            self.assertIn(region, response)

            for itype in expected[region]:
                # Instance type must be present in expected region
                self.assertIn(itype, response[region])
                # Counts must match
                self.assertEquals(
                        expected[region][itype],
                        response[region][itype]
                    )

    def test_aggregate_type(self):
        pass

    '''
    Method should only accept GET
    '''
    def test_aggregate_methods(self):
        pass

    '''
    Method should return Bad Request if filter is not a region or type
    '''
    def test_aggregate_filter(self):
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
