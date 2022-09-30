import unittest
from drivenc import drivenc
from pprint import pprint



class MyTestCase(unittest.TestCase):
    def test_cameras(self):
        uut = drivenc()
        uut.camera_list()
        self.assertGreaterEqual(len(uut.cameras), 600)

    def test_incidents(self):
        uut = drivenc()
        incidents = uut.incidents()
        self.assertGreaterEqual(len(incidents['activeIncidents']), 99)


if __name__ == '__main__':
    unittest.main()
