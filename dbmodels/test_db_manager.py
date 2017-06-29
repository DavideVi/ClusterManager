import unittest
from db_manager import DBManager

class TestDBManager(unittest.TestCase):

    def test_create(self):
        db = DBManager('endpoint')

    def test_singleton(self):
        # Creating two instance
        x = DBManager('a')
        y = DBManager('b')

        # Initial instance should have been changed as
        # a result of second instance param
        self.assertEqual(x.endpoint, 'b')

if __name__ == '__main__':
    unittest.main()
