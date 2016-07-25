import unittest
import os
from gen_data_simple import makedata
from check_data_DB import send_notif
from check_data_DB import check_data

class makedataTest(unittest.TestCase):

    def testmakedata(self):
        f1,f2,f3,findx = makedata()
        self.assertIsNotNone(f1)
        self.assertIsNotNone(f2)
        self.assertIsNotNone(f3)
        self.assertIsNotNone(findx)


class checkdataDBTest(unittest.TestCase):

    def testsendnotif(self):
        a,b = send_notif(1,1)
        self.assertEqual(a, 'Outliers!')
        self.assertEqual(b, 'Miscalibration!')

    def testcheckdata(self):
        z, x, y = check_data(5, "./static/images/")
        self.assertIsNotNone(z)
        self.assertIsNotNone(x)
        self.assertIsNotNone(y)
        self.assertTrue(os.path.isfile("./MultiShuttle.db"))
        self.assertTrue(os.path.isfile("./static/images/df.png"))
        self.assertTrue(os.path.isfile("./static/images/calx.png"))
        self.assertTrue(os.path.isfile("./static/images/caly.png"))

def main():
    unittest.main()

if __name__ == '__main__':
    main()
